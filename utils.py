# from PySide6.QtCore import Qt
# from PySide6.QtGui import QFont
import json
import os
import logging
import argparse
from waveshare_lib import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
picdir = os.path.join("waveshare_lib/pic")
import time
import textwrap
import tempfile
import shutil
import RPi.GPIO as GPIO

def print_highlight(text):
    print("\n")
    print("-----------------------------------------------------------------------------")
    print("--------\t" + text)
    print()


def get_book_name():
    parser = argparse.ArgumentParser(description="Read a book.")
    parser.add_argument("-b", "--book",
                    type=str,
                    help="The name of the book to read")

    args = parser.parse_args()
    if args.book:
        return args.book
    print("Opening default book: 1984")
    return "1984"


def clear_epd(epd):
	logging.info("Clear...")
	epd.init()
	epd.Clear()


def sleep_epd(epd):
	logging.info("Goto Sleep...")
	epd.sleep()
	print("Ready")


def average_font_width(font):
    characters = " abcdefghijklmnopqrstuvwxyz"
    # characters = " abcdefghijklmnopqrstuvwxyz,.;-...°#~`!@#$%^&*()_+{}[]|\\:\"<>?/'"
    width = font.getlength(characters)
    return width / len(characters)


def fit_text_within_screen(text, font, margins, width, font_size, filepath, fast_mode):
    lines = []
    text_width = width - 2 * margins - font_size/2
    paragraphs = text.split("\n")

    # Load word widths from file
    meta_dir = os.path.join(filepath, "meta")
    os.makedirs(meta_dir, exist_ok=True)  # Create the directory if it does not exist
    try:
        with open(f"{filepath}/meta/word_widths.json", "r") as f:
            word_widths = json.load(f)
    except FileNotFoundError:
        word_widths = {}

    for paragraph in paragraphs:
        if fast_mode:
            wrapper_width = text_width / average_font_width(font)
            wrapped_paragraph = textwrap.wrap(paragraph, width=wrapper_width, initial_indent="    ")
            lines.extend(wrapped_paragraph)
        else:
            line = ""
            first_word = True
            for word in paragraph.split():
                if first_word:
                    word = "    " + word
                    first_word = False
                if word not in word_widths:
                    word_widths[word] = font.getbbox(word)[2]
                if word_widths[word] + (font.getbbox(line)[2] if line else 0) > text_width:
                    lines.append(line)
                    line = word
                else:
                    line = line + " " + word if line else word
            lines.append(line)

    # Save word widths to file
    with open(f"{filepath}/meta/word_widths.json", "w") as f:
        json.dump(word_widths, f)

    return lines


def load_index(filepath):
    index_file = os.path.join(f"{filepath}/meta", "index.txt")
    if os.path.exists(index_file):
        print("Loading existing index")
        with open(index_file, "r") as file:
            return json.load(file)
    else:
        return 1  # Default index


def save_index(filepath, old_index):
    meta_dir = os.path.join(filepath, "meta")
    os.makedirs(meta_dir, exist_ok=True)  # Create the directory if it does not exist
    index_file = os.path.join(meta_dir, "index.txt")
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    try:
        with open(temp_file.name, 'w') as file:
            json.dump(old_index, file)
            file.flush()  # Flush the buffer
            os.fsync(file.fileno())  # Force write to disk
    except Exception as e:
        print(f"Error while writing to temporary file: {e}")
    else:
        shutil.move(temp_file.name, index_file)  # Replace the old file with the new file


def error_screen(err):
    # Parameters
    FONT_SIZE = 25
    FONT = ImageFont.truetype(os.path.join(picdir, "arial.ttf"), FONT_SIZE)

    # Setup epaper display
    logging.info("init and Clear")
    epd = epd7in5_V2.EPD()
    width = epd.width
    height = epd.height

    epd.init()
    ScreenImage = Image.new("1", (width, height), 255)
    screen_buffer = ImageDraw.Draw(ScreenImage)
    screen_buffer.text((0,FONT_SIZE*0), f"Error: {err}", font=FONT, fill=0)
    screen_buffer.text((0,FONT_SIZE*2), "Please refer to GitHub for more info.", font=FONT, fill=0)
    screen_buffer.text((0,FONT_SIZE*3), "(or ask Alessandro)", font=FONT, fill=0)

    # Update screen
    epd.display(epd.getbuffer(ScreenImage))
    sleep_epd(epd)

    while True:
        print("Sleep...")
        time.sleep(1984)


def get_closest_heading(index, filepath):
    headings_file = os.path.join(f"{filepath}/meta", "headings.json")
    with open(headings_file, "r") as f:
        headings = json.load(f)

    headings = {int(k): v for k, v in headings.items()}
    possible_headings = [i for i in headings if i >= index]

    if not possible_headings:
        return "Last Chapter"

    closest_heading_index = min(possible_headings)
    left_paragraphs = closest_heading_index - index
    next_paragraph = headings[closest_heading_index]["text"]

    return f"{left_paragraphs} until {next_paragraph}"


def handle_switch(reader, epd):
    switch_state = get_switch_state(reader.SWITCH_GPIO)
    double_switch_event = False

    if switch_state != reader.last_switch_state:
        t = time.time()
        while time.time() - t < 0.8:
            if get_switch_state(reader.SWITCH_GPIO) != switch_state:
                double_switch_event = True
        if double_switch_event:
            print_highlight("Previous page")
            reader.show_previous_screen(epd)
        else:
            print_highlight("Next page")
            reader.show_next_screen(epd)

    reader.last_switch_state = get_switch_state(reader.SWITCH_GPIO)
    time.sleep(0.25)

def get_switch_state(gpio):
    return GPIO.input(gpio)

# class ContentFormatter:
#     def __init__(self):
#         self.last_class_type = None
#         self.class_types = {
#             'Class: Title': (QFont('Arial', 60), Qt.AlignJustify, False),
#             'Class: Author': (QFont('Arial', 30), Qt.AlignJustify, False),
#             'Class: Heading-1': (QFont('Arial', 30), Qt.AlignJustify, False),
#             'Class: Heading-2': (QFont('Arial', 25), Qt.AlignJustify, False),
#             'Class: Paragraph---First': (QFont('Arial', 20), Qt.AlignJustify, False),
#             'Class: Paragraph---Indent': (QFont('Arial', 20), Qt.AlignJustify, False),
#             'Class: Paragraph---Blockquote': (QFont('Arial', 20), Qt.AlignJustify, True),
#             'Class: default': (QFont('Arial', 20), Qt.AlignJustify, False)
#         }

#     def content_format(self, content):
#         lines = content.split('\n')
#         class_line = lines[0]
#         text_content = '\n\t'.join(lines[1:])

#         if any(class_type in class_line for class_type in self.class_types):
#             self.last_class_type = class_line
#         else:
#             text_content = content
#             class_line = self.last_class_type if self.last_class_type else 'default'

#         font, alignment, font_italic = self.class_types[class_line]

#         if class_line == 'Class: Paragraph---First':
#             text_content = '\t' + text_content
#         if class_line == 'Class: Paragraph---Blockquote':
#             text_content = '\n' + text_content + '\n'

#         return font, alignment, text_content, font_italic

