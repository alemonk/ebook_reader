import sys
import os
picdir = os.path.join("waveshare_lib/pic")
import logging
from waveshare_lib import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont


def clear_epd(epd):
    logging.info("Clear...")
    epd.init()
    epd.Clear()


def sleep_epd(epd):
	logging.info("Goto Sleep...")
	epd.sleep()


def fit_text_within_screen(text, font, epd, margins):
    lines = []
    line = ""
    text_width = epd.height - 2 * margins
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
	with open(os.path.join(f"epubs_parsed/{book}", f"{i}.txt"), "r") as file:
		content = file.read()
	print(f"Opening file {i}")
	return content


def show_next_screen(epd, x_cursor, y_cursor, overflow_lines=""):
	print("++++++++++++++++++++++++++++++++")
	global index
	# clear_epd(epd)
	ScreenImage = Image.new("1", (epd.height, epd.width), 255)
	screen_buffer = ImageDraw.Draw(ScreenImage)
	text_height = epd.width - 2 * margins
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
	epd.display(epd.getbuffer(ScreenImage))
	return extra_lines


logging.basicConfig(level=logging.DEBUG)
try:
	# Parameters
	margins = 5
	x = margins
	y = margins
	font_size = 25
	line_space = 1
	font = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), font_size)
	
	index = 0
	book = "1984"
    
    # Setup epaper display
	logging.info("init and Clear")
	epd = epd7in5_V2.EPD()
	clear_epd(epd)
	
	extra_lines = show_next_screen(epd, x, y)
	
	for _ in range(10):
		time.sleep(0.5)
		extra_lines = show_next_screen(epd, x, y, extra_lines)

	sleep_epd(epd)

except IOError as e:
	logging.info(e)
except KeyboardInterrupt:    
	logging.info("ctrl + c:")
	epd7in5_V2.epdconfig.module_exit(cleanup=True)
	exit()
