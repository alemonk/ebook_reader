import os
import logging
from waveshare_lib import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import RPi.GPIO as GPIO
from utils import *
import textwrap

class EBookReader:
	def __init__(self):
		self.VERTICAL = False
		self.MARGINS = 0
		self.FONT_SIZE = 25
		self.PARAGRAPH_SPACE = 5
		self.BUTTOM_BCM = 26
		self.DEBOUNCE_PERIOD = 0.3
		self.picdir = os.path.join("waveshare_lib/pic")
		self.FONT = ImageFont.truetype(os.path.join(self.picdir, "arial.ttf"), self.FONT_SIZE)
		self.index = 0
		self.old_index = 0
		self.extra_lines = ""
		self.filepath = ""
		self.book = ""
		self.width = 0
		self.height = 0
		self.contents = {}

	def store_content(self):
		for i in os.listdir(self.filepath):
			full_path = os.path.join(self.filepath, i)
			if os.path.isfile(full_path):
				with open(full_path, "r") as file:
						self.contents[i] = file.read()

	def get_content(self, i):
		content = self.contents.get(f"{i}.txt")
		if content is None:
			content = "E N D O F C O N T E N T " * 50
			print(f"File {i} not found, returning default content")
		else:
			print(f"Opening file {i}")
		return content
	
	def button_pressed_animation(self):
		epd.init_part()
		Himage = Image.new('1', (epd.width, epd.height), 0)
		draw = ImageDraw.Draw(Himage)
		draw.rectangle((self.width-10, self.height-10, self.width, self.height), fill = 255)
		epd.display_Partial(epd.getbuffer(Himage),0, 0, self.width, self.height)

	def show_next_screen(self, epd, overflow_lines=""):
		self.old_index = self.index
		x_cursor = self.MARGINS
		y_cursor = self.MARGINS

		epd.init_fast()
		ScreenImage = Image.new("1", (self.width, self.height), 255)
		screen_buffer = ImageDraw.Draw(ScreenImage)
		text_height = self.height - 2 * self.MARGINS - self.FONT_SIZE
		extra_lines = []

		if overflow_lines:
			for _, line in enumerate(overflow_lines):
				if y_cursor > text_height - self.FONT_SIZE:
					extra_lines.append(line)
				else:
					# print(line)
					screen_buffer.text((x_cursor,y_cursor), line, font=self.FONT, fill=0)
					y_cursor += self.FONT_SIZE

		while y_cursor <= text_height - self.FONT_SIZE:
			y_cursor += self.PARAGRAPH_SPACE
			content = self.get_content(self.index)
			lines = fit_text_within_screen(content, self.FONT, self.MARGINS, self.width, self.FONT_SIZE, self.filepath)
			for _, line in enumerate(lines):
				if y_cursor > text_height - self.FONT_SIZE:
					extra_lines.append(line)
				else:
					# print(line)
					screen_buffer.text((x_cursor,y_cursor), line, font=self.FONT, fill=0)
					y_cursor += self.FONT_SIZE
			self.index += 1

		save_index(self.filepath, self.old_index)

		# Progress bar
		lst = os.listdir(self.filepath)
		n_files = len(lst) - 1
		progress = f"Page {self.old_index}/{n_files} - {str(round(100 * self.old_index/n_files, 2))} %"
		progress_width = self.width * self.old_index / n_files
		font_small = ImageFont.truetype(os.path.join(self.picdir, "arial.ttf"), self.FONT_SIZE-5)
		screen_buffer.rectangle((0, self.height-4, progress_width, self.height), fill=0)
		screen_buffer.text((round(self.MARGINS/2), self.height-self.FONT_SIZE-round(self.MARGINS/2)), progress, font=font_small, fill=0)

		# Update screen
		epd.display(epd.getbuffer(ScreenImage))
		sleep_epd(epd)
		return extra_lines

	def show_previous_screen(self, epd):
		self.index = self.old_index - 1
		if self.index <= 0:
			self.index = 1
		return self.show_next_screen(epd)


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	try:
		reader = EBookReader()
		# Setup epaper display
		logging.info("init and Clear")
		epd = epd7in5_V2.EPD()
		clear_epd(epd)
		reader.width = epd.height if reader.VERTICAL else epd.width
		reader.height = epd.width if reader.VERTICAL else epd.height

		# Variables
		book = get_book_name()
		reader.filepath = "parsed_epubs/" + book
		reader.index = load_index(reader.filepath)
		reader.old_index = 0
		extra_lines = ""

		# Setup button
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(reader.BUTTOM_BCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# Open book
		reader.store_content()
		extra_lines = reader.show_next_screen(epd)

		while True:
			double_click_event = False

			if GPIO.input(reader.BUTTOM_BCM) == GPIO.HIGH:
				# reader.button_pressed_animation()
				t = time.time()
				time.sleep(reader.DEBOUNCE_PERIOD)
				while time.time() - t < (0.8 - reader.DEBOUNCE_PERIOD):
					if GPIO.input(reader.BUTTOM_BCM) == GPIO.HIGH:
						double_click_event = True
				if double_click_event:
					print_highlight("Previous page")
					extra_lines = reader.show_previous_screen(epd)
				else:
					print_highlight("Next page")
					extra_lines = reader.show_next_screen(epd, extra_lines)

				# print_highlight("Next page")
				# extra_lines = reader.show_next_screen(epd, extra_lines)
			time.sleep(0.25)

	except Exception as e:
		logging.info(e)
		error_screen(e)
	except KeyboardInterrupt:
		logging.info("ctrl + c:")
		print("GPIO cleanup")
		print("epd cleanup")
		GPIO.cleanup()
		epd7in5_V2.epdconfig.module_exit(cleanup=True)
		exit()

