import logging
from waveshare_lib import epd7in5_V2
from gpiozero import Button
from utils import *
from EBookReader import EBookReader
import time

def setup_epaper_display():
    logging.info('init and Clear')
    epd = epd7in5_V2.EPD()
    clear_epd(epd)
    return epd

def handle_switch(reader, epd, switch):
    switch_state = switch.is_pressed
    double_switch_event = False

    if switch_state != reader.last_switch_state:
        t = time.time()
        reader.last_switch_toggle_time = t
        while time.time() - t < 0.8:
            if switch.is_pressed != switch_state:
                double_switch_event = True
        if double_switch_event:
            print_highlight('Previous page')
            reader.load_previous_screen()
            reader.update_screen(epd)
            reader.load_next_screen()
        else:
            print_highlight('Next page')
            reader.update_screen(epd)
            reader.load_next_screen()

    reader.last_switch_state = switch.is_pressed

def print_quote(reader, epd):
    reader.index = reader.old_index
    reader.extra_lines = []
    clear_epd(epd)
    quote = get_quotes(random=True)
    message = f"{quote['data'][0]['quote']} \n - {quote['data'][0]['author']}"
    print_on_epd(epd=epd, reader=reader, message=message)
    if get_switch_state(switch):
        switch.wait_for_inactive()
    else:
        switch.wait_for_active()
    reader.last_switch_toggle_time = time.time()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        # Setup epaper display
        epd = setup_epaper_display()

        # Setup interface
        reader = EBookReader(epd)
        reader.width = epd.height if reader.VERTICAL else epd.width
        reader.height = epd.width if reader.VERTICAL else epd.height
        if reader.SCREENSAVER_QUOTES:
            from quotes_library import get_quotes

        # Variables
        book = get_book_name()
        reader.filepath = 'parsed_epubs/' + book
        reader.index = load_index(reader.filepath)
        reader.old_index = 0

        # Setup button
        switch = Button(reader.SWITCH_GPIO)
        reader.set_last_switch_state(get_switch_state(switch))

        # Open book
        reader.store_content()
        reader.load_next_screen()
        reader.update_screen(epd)
        reader.load_next_screen()

        network_disabled = False

        while True:
            handle_switch(reader, epd, switch)

            if time.time() - reader.last_switch_toggle_time > 60 * 60:
                if not network_disabled:
                    disable_network()
                    network_disabled = True
                if reader.SCREENSAVER_QUOTES:
                    print_quote(reader, epd)
            else:
                if network_disabled:
                    enable_network()
                    network_disabled = False

            time.sleep(0.25)

    # except Exception as e:
    #     logging.info(e)
    #     print_on_epd(epd, reader, str(e))
    except KeyboardInterrupt:
        logging.info('ctrl + c:')
        print_highlight('GPIO and epd cleanup')
        reader.switch.close()
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        exit()
