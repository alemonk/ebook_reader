import logging
from waveshare_lib import epd7in5_V2
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

        # Setup button
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(reader.SWITCH_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        reader.set_initial_switch_state()

        # Open book
        reader.store_content()
        # ScreenImage = reader.show_next_screen(epd)

        while True:
            handle_switch(reader, epd)

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
