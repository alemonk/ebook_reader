import sys
sys.path.insert(0, '/home/alekappe/ebook_reader')
import os
import logging
from waveshare_lib import epd7in5_V2
from utils import sleep_epd
from PIL import Image,ImageDraw,ImageFont
picdir = os.path.join("waveshare_lib/pic")
import time

# Parameters
FONT_SIZE = 40
FONT = ImageFont.truetype(os.path.join(picdir, "arial.ttf"), FONT_SIZE)

# Setup epaper display
logging.info("init and Clear")
epd = epd7in5_V2.EPD()
width = epd.width
height = epd.height

epd.init()
ScreenImage = Image.new("1", (width, height), 255)
screen_buffer = ImageDraw.Draw(ScreenImage)
screen_buffer.text((0,0), "Very very very long sentece that cannot fit within epd.width pixels", font=FONT, fill=0)

# Update screen
epd.display(epd.getbuffer(ScreenImage))
sleep_epd(epd)

while True:
    print("Sleep...")
    time.sleep(1984)
