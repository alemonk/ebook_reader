import logging
from waveshare_lib import epd7in5_V2
from gpiozero import Button
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
        switch = Button(reader.SWITCH_GPIO)
        reader.set_last_switch_state(get_switch_state(switch))

        # Open book
        reader.store_content()
        ScreenImage = reader.show_next_screen(epd)

        while True:
            handle_switch(reader, epd, switch)

    except Exception as e:
        logging.info(e)
        error_screen(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        print("GPIO cleanup")
        print("epd cleanup")
        reader.switch.close()
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        exit()
