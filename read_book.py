import sys
import os
picdir = os.path.join('waveshare_lib/pic')
import logging
from waveshare_lib import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def fit_text_within_screen(text, font18, epd):
	lines = []
	line = ""
	for word in text.split():
		if font18.getbbox(line + " " + word)[2] > epd.height * 0.9:
			lines.append(line)
			line = word
		else:
			line = line + " " + word if line else word
	lines.append(line)
	return lines


try:
	logging.info("epd7in5_V2 Demo")
	epd = epd7in5_V2.EPD()
    
	logging.info("init and Clear")
	epd.init()
	epd.Clear()

	font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
	font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

	x = 10
	y = 10
	text = '1some really long text 2some really long text 3some really long text 4some really long text 5some really long text'
	lines = fit_text_within_screen(text, font18, epd)
	    
	# Drawing on the Vertical image
	logging.info("2.Drawing on the Vertical image...")
	epd.init()
	ScreenImage = Image.new('1', (epd.height, epd.width), 255)
	screen_buffer = ImageDraw.Draw(ScreenImage)
	for i, line in enumerate(lines):
		screen_buffer.text((x,y), line, font=font18, fill=0)
		y += 18
	epd.display(epd.getbuffer(ScreenImage))
	time.sleep(2)

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()

	logging.info("Goto Sleep...")
	epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
