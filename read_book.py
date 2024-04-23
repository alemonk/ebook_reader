import sys
import os
picdir = os.path.join("waveshare_lib/pic")
import logging
from waveshare_lib import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import RPi.GPIO as GPIO
from utils import *


def clear_epd(epd):
    logging.info("Clear...")
    epd.init()
    epd.Clear()


def sleep_epd(epd):
	logging.info("Goto Sleep...")
	epd.sleep()
	print("Ready")


def fit_text_within_screen(text, font, epd, margins):
    lines = []
    line = ""
    text_width = width - 2 * margins
    for word in text.split():
        word_width = font.getbbox(word)[2]
        if word_width + font.getbbox(line)[2] > text_width:
            lines.append(line)
            line = word
        else:
            line = line + " " + word if line else word
    lines.append(line)
    return lines


def get_content(i):
	with open(os.path.join(f"{filepath}", f"{i}.txt"), "r") as file:
		content = file.read()
	print(f"Opening file {i}")
	# print(content)
	return content


def show_next_screen(epd, x_cursor, y_cursor, overflow_lines=""):
	global index
	global old_index

	old_index = index

	epd.init_fast()
	ScreenImage = Image.new("1", (width, height), 255)
	screen_buffer = ImageDraw.Draw(ScreenImage)
	text_height = height - 2 * margins - font_size
	extra_lines = []

	if overflow_lines:
		for _, line in enumerate(overflow_lines):
			if y_cursor > text_height - font_size:
				extra_lines.append(line)
			else:
				# print(line)
				screen_buffer.text((x_cursor,y_cursor), line, font=font, fill=0)
				y_cursor += font_size + line_space

	while y_cursor <= text_height - font_size:
		index += 1
		content = get_content(index)
		lines = fit_text_within_screen(content, font, epd, margins)
		for _, line in enumerate(lines):
			if y_cursor > text_height - font_size:
				extra_lines.append(line)
			else:
				# print(line)
				screen_buffer.text((x_cursor,y_cursor), line, font=font, fill=0)
				y_cursor += font_size + line_space

	# Progress bar
	lst = os.listdir(filepath)
	n_files = len(lst) - 1
	progress = str(round(100 * index/n_files, 2)) + f" % - page {index}/{n_files}"
	progress_width = width * index / n_files
	font_small = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), font_size-5)
	screen_buffer.rectangle((0,height-4,progress_width,height), fill=0)
	screen_buffer.text((round(margins/2),height-font_size-round(margins/2)), progress, font=font_small, fill=0)

	# Update screen
	epd.display(epd.getbuffer(ScreenImage))
	sleep_epd(epd)
	save_index(filepath, old_index)
	return extra_lines


def show_previous_screen(epd, x, y):
	global index
	global old_index

	index = old_index - 3
	if index < 0:
		index = 0
	return show_next_screen(epd, x, y)


logging.basicConfig(level=logging.DEBUG)
try:
    # Setup epaper display
	logging.info("init and Clear")
	epd = epd7in5_V2.EPD()
	clear_epd(epd)

	# Parameters and variables
	book = "1984"
	filepath = "parsed_epubs/" + book
	margins = 0
	width = epd.width
	height = epd.height
	font_size = 25
	line_space = 1
	n_button = 26
	debounce_period = 0.2
	font = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), font_size)
	x = margins
	y = margins
	index = load_index(filepath)
	# index = 0
	old_index = 0
	extra_lines = ""

	# Setup buttons
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(n_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	# while True:
	# 	extra_lines = show_next_screen(epd, x, y, extra_lines)
	# ScreenImage = Image.new("1", (width, height), 255)
	extra_lines = show_next_screen(epd, x, y)

	while True:
		double_click_event = False

		if GPIO.input(n_button) == GPIO.HIGH:
			t = time.time()
			time.sleep(debounce_period)

			while time.time() - t < (0.8 - debounce_period):
				if GPIO.input(n_button) == GPIO.HIGH:
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

