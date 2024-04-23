import sys
import os
picdir = os.path.join("waveshare_lib/pic")
import logging
from waveshare_lib import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import RPi.GPIO as GPIO
from utils import *

# Parameters
VERTICAL = False
MARGINS = 0
FONT_SIZE = 25
PARAGRAPH_SPACE = 5
BUTTOM_BCM = 26
DEBOUNCE_PERIOD = 0.2
FONT = ImageFont.truetype(os.path.join(picdir, "arial.ttf"), FONT_SIZE)

def get_content(i):
	try:
		with open(os.path.join(f"{filepath}", f"{i}.txt"), "r") as file:
			content = file.read()
		print(f"Opening file {i}")
	except FileNotFoundError:
		content = "T H E _ E N D _ " * 100
		print(f"File {i} not found, returning default content")
	return content


def show_next_screen(epd, x_cursor, y_cursor, overflow_lines=""):
	global index
	global old_index

	old_index = index

	epd.init_fast()
	ScreenImage = Image.new("1", (width, height), 255)
	screen_buffer = ImageDraw.Draw(ScreenImage)
	text_height = height - 2 * MARGINS - FONT_SIZE
	extra_lines = []

	if overflow_lines:
		for _, line in enumerate(overflow_lines):
			if y_cursor > text_height - FONT_SIZE:
				extra_lines.append(line)
			else:
				# print(line)
				screen_buffer.text((x_cursor,y_cursor), line, font=FONT, fill=0)
				y_cursor += FONT_SIZE

	while y_cursor <= text_height - FONT_SIZE:
		y_cursor += PARAGRAPH_SPACE
		content = get_content(index)
		lines = fit_text_within_screen(content, FONT, MARGINS, width, FONT_SIZE)
		for _, line in enumerate(lines):
			if y_cursor > text_height - FONT_SIZE:
				extra_lines.append(line)
			else:
				# print(line)
				screen_buffer.text((x_cursor,y_cursor), line, font=FONT, fill=0)
				y_cursor += FONT_SIZE
		index += 1

	save_index(filepath, old_index)

	# Progress bar
	lst = os.listdir(filepath)
	n_files = len(lst) - 1
	progress = f"Page {old_index}/{n_files} - {str(round(100 * old_index/n_files, 2))} %"
	progress_width = width * old_index / n_files
	font_small = ImageFont.truetype(os.path.join(picdir, "arial.ttf"), FONT_SIZE-5)
	screen_buffer.rectangle((0,height-4,progress_width,height), fill=0)
	screen_buffer.text((round(MARGINS/2),height-FONT_SIZE-round(MARGINS/2)), progress, font=font_small, fill=0)

	# Update screen
	epd.display(epd.getbuffer(ScreenImage))
	sleep_epd(epd)
	return extra_lines


def show_previous_screen(epd, x, y):
	global index
	global old_index

	index = old_index - 1
	if index <= 0:
		index = 1
	return show_next_screen(epd, x, y)


logging.basicConfig(level=logging.DEBUG)
try:
	# Setup epaper display
	logging.info("init and Clear")
	epd = epd7in5_V2.EPD()
	clear_epd(epd)
	width = epd.height if VERTICAL else epd.width
	height = epd.width if VERTICAL else epd.height

	# Variables
	book = get_book_name()
	filepath = "parsed_epubs/" + book
	x = MARGINS
	y = MARGINS
	index = load_index(filepath)
	old_index = 0
	extra_lines = ""

	# Setup button
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BUTTOM_BCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	# Open book
	extra_lines = show_next_screen(epd, x, y)

	while True:
		double_click_event = False

		if GPIO.input(BUTTOM_BCM) == GPIO.HIGH:
			t = time.time()
			time.sleep(DEBOUNCE_PERIOD)

			while time.time() - t < (0.8 - DEBOUNCE_PERIOD):
				if GPIO.input(BUTTOM_BCM) == GPIO.HIGH:
					double_click_event = True

			if double_click_event:
				print_highlight("Previous page")
				extra_lines = show_previous_screen(epd, x, y)
			else:
				print_highlight("Next page")
				extra_lines = show_next_screen(epd, x, y, extra_lines)

except IOError as e:
	logging.info(e)
except KeyboardInterrupt:
	logging.info("ctrl + c:")
	print("GPIO cleanup")
	print("epd cleanup")
	GPIO.cleanup()
	epd7in5_V2.epdconfig.module_exit(cleanup=True)
	exit()

