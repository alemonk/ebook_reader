import logging
from waveshare_lib import epd7in5_V2
import time
import RPi.GPIO as GPIO
from utils import *
from EBookReader import EBookReader


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
		extra_lines = ""

		# Setup button
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(reader.BUTTOM_BCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# Open book
		reader.store_content()
		extra_lines, ScreenImage = reader.show_next_screen(epd)

		while True:
			double_click_event = False

			if GPIO.input(reader.BUTTOM_BCM) == GPIO.HIGH:
				t = time.time()
				time.sleep(reader.DEBOUNCE_PERIOD)
				while time.time() - t < (0.8 - reader.DEBOUNCE_PERIOD):
					if GPIO.input(reader.BUTTOM_BCM) == GPIO.HIGH:
						double_click_event = True
				if double_click_event:
					print_highlight("Previous page")
					reader.button_pressed_animation(ScreenImage, text="Previous page")
					extra_lines, ScreenImage = reader.show_previous_screen(epd)
				else:
					print_highlight("Next page")
					reader.button_pressed_animation(ScreenImage, text="Next page")
					extra_lines, ScreenImage = reader.show_next_screen(epd, extra_lines)

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
