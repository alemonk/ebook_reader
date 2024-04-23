# from PySide6.QtCore import Qt
# from PySide6.QtGui import QFont
import json
import os
import logging

def print_highlight(text):
    print('\n')
    print('-----------------------------------------------------------------------------')
    print('--------\t' + text)
    print()


def clear_epd(epd):
	logging.info("Clear...")
	epd.init()
	epd.Clear()


def sleep_epd(epd):
	logging.info("Goto Sleep...")
	epd.sleep()
	print("Ready")


def fit_text_within_screen(text, font, margins, width, font_size):
	lines = []
	line = ""
	text_width = width - 2 * margins - font_size/2 # Added font_size/2 to prevent overshoot if margins are tiny
	first_word = True
	for word in text.split():
		if first_word:
			word = "    " + word
			first_word = False
		if word != "__newline__":
			word_width = font.getbbox(word)[2]
			if word_width + font.getbbox(line)[2] > text_width:
				lines.append(line)
				line = word
			else:
				line = line + " " + word if line else word
		else:
			lines.append(line)
			line = ""
	lines.append(line)
	return lines


def load_index(filepath):
    index_file = os.path.join(filepath, 'index.txt')
    if os.path.exists(index_file):
        print("Loading existing index")
        with open(index_file, 'r') as file:
            return json.load(file)
    else:
        return 0  # Default index


def save_index(filepath, old_index):
    index_file = os.path.join(filepath, 'index.txt')
    with open(index_file, 'w') as file:
        json.dump(old_index, file)


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
