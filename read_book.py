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
    total_text_width = epd.height - 2 * margins
    for word in text.split():
        word_width = font.getbbox(word)[2]
        if word_width + font.getbbox(line)[2] > total_text_width:
            lines.append(line)
            line = word
        else:
            line = line + " " + word if line else word
    lines.append(line)
    return lines


def get_content(i):
	with open(os.path.join(f"epubs_parsed/{book}", f"{i}.txt"), "r") as file:
		content = file.read()
	return content


def show_next_screen(epd, x_cursor, y_cursor):
	clear_epd(epd)
	ScreenImage = Image.new("1", (epd.height, epd.width), 255)
	screen_buffer = ImageDraw.Draw(ScreenImage)
	for i in range(1,7):
		content = get_content(i)
		lines = fit_text_within_screen(content, font, epd, margins)
		for i, line in enumerate(lines):
			print(line)
			screen_buffer.text((x_cursor,y_cursor), line, font=font, fill=0)
			y_cursor += font_size
	epd.display(epd.getbuffer(ScreenImage))


logging.basicConfig(level=logging.DEBUG)
try:
	# Parameters
	margins = 10
	x = margins
	y = margins
	font_size = 24
	font = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), font_size)
	book = "1984"
    
    # Setup epaper display
	logging.info("init and Clear")
	epd = epd7in5_V2.EPD()
	
	show_next_screen(epd, x, y)

	sleep_epd(epd)

except IOError as e:
	logging.info(e)
except KeyboardInterrupt:    
	logging.info("ctrl + c:")
	epd7in5_V2.epdconfig.module_exit(cleanup=True)
	exit()
