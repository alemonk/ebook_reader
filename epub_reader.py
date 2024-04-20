from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QFontMetrics, QTextCursor
from key_press_handler import *
import os
from utils import *
import math

class EpubReader(QWidget):
    def __init__(self, filepath, width, height, border):
        super().__init__()

        self.setObjectName(filepath.capitalize())
        self.filepath = 'epubs_parsed/' + filepath
        self.files = sorted([f for f in os.listdir(self.filepath) if f.split('.')[0].isdigit()], key=lambda x: int(x.split('.')[0]))
        self.index = load_index(self.filepath)
        self.old_index = 0
        self.is_overflow = False
        self.overflow_text = ''
        self.formatter = ContentFormatter()

        self.text_widget = QTextEdit(self)
        self.text_widget.setReadOnly(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(width, height)
        self.key_press_handler = KeyPressHandler(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_widget)
        layout.setContentsMargins(border, border, border, border)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        self.key_press_handler.handle_key_press(event)

    def show_next(self):
        # os.system('clear')
        self.is_overflow = False
        self.old_index = self.index
        self.text_widget.clear()
        while self.index < len(self.files) and self.is_overflow == False:
            content = self.get_content()
            self.append_content_to_widget(content)
            while self.num_overflow_lines() > 0:
                self.remove_last_char_from_widget()
        save_index(self.filepath, self.old_index)

    def get_content(self):
        if self.overflow_text != '':
            content = self.formatter.content_format(self.overflow_text)
            print('finishing to print file: ', self.files[self.index-1])
            # print(self.overflow_text)
            self.overflow_text = ''
        else:
            with open(os.path.join(self.filepath, self.files[self.index]), 'r') as file:
                print('opening file: ', self.files[self.index])
                self.index += 1
                content = self.formatter.content_format(file.read())
        return content

    def append_content_to_widget(self, content):
        font, alignment, text_content, font_italic = content
        # print('text_content: ', text_content)
        text_content = text_content
        format = QTextCharFormat()
        format.setFont(font)
        format.setFontItalic(font_italic)
        cursor = self.text_widget.textCursor()
        cursor.setCharFormat(format)
        cursor.insertText(text_content)
        self.text_widget.setAlignment(alignment)

    def num_overflow_lines(self):
        doc_height = self.text_widget.document().size().height()
        viewport_height = self.text_widget.viewport().height()
        overflow = doc_height - viewport_height

        font_metrics = QFontMetrics(self.text_widget.currentFont())
        line_height = font_metrics.lineSpacing()
        num_lines = math.ceil(overflow / line_height)
        if num_lines > 0:
            self.is_overflow = True
            # print('OVERFLOW, by ', num_lines, ' lines')
        return num_lines

    def remove_last_char_from_widget(self):
        cursor = self.text_widget.textCursor()
        cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)  # Select the previous character
        char = cursor.selectedText()  # Get the selected character
        self.overflow_text = char + self.overflow_text  # Prepend the character to overflow_text
        cursor.removeSelectedText()  # Remove the selected character
        self.text_widget.setTextCursor(cursor)

    def show_previous(self):
        self.index = self.old_index - 1
        self.overflow_text = ''
        self.show_next()
