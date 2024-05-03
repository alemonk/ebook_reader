import logging
from waveshare_lib import epd7in5_V2
import time
import RPi.GPIO as GPIO
from utils import *
from EBookReader import EBookReader

def handle_switch(reader, ScreenImage):
	switch_state = GPIO.input(reader.BUTTOM_BCM)
	double_switch_event = False

	if switch_state != reader.last_switch_state:
		t = time.time()
		while time.time() - t < 0.8:
			if GPIO.input(reader.BUTTOM_BCM) != switch_state:
				double_switch_event = True
		if double_switch_event:
			print_highlight("Previous page")
			ScreenImage = reader.show_previous_screen(epd)
		else:
			print_highlight("Next page")
			ScreenImage = reader.show_next_screen(epd)

	reader.last_switch_state = GPIO.input(reader.BUTTOM_BCM)
	time.sleep(0.25)
	return ScreenImage

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        # Setup epaper display
        logging.info("init and Clear")
        epd = epd7in5_V2.EPD()
        clear_epd(epd)

        # Setup interface
        reader = EBookReader(epd)
        reader.width = epd.height if reader.VERTICAL else epd.width
        reader.height = epd.width if reader.VERTICAL else epd.height

        # Variables
        book = get_book_name()
        reader.filepath = "parsed_epubs/" + book
        reader.index = load_index(reader.filepath)
        reader.old_index = 0

        # Setup button
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(reader.BUTTOM_BCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Open book
        reader.store_content()
        ScreenImage = reader.show_next_screen(epd)

        while True:
            ScreenImage = handle_switch(reader, ScreenImage)

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
