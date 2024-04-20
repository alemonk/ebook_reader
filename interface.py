from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from epub_reader import *
import sys
import os
from key_press_handler import *

class BookSelector(QWidget):
    def __init__(self, directory, width, height, border):
        super().__init__()

        self.setObjectName('HOME_MENU')
        self.directory = directory
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(width, height)
        self.key_press_handler = KeyPressHandler(self)

        self.populate_list()

        self.layout.addWidget(self.list_widget)
        self.layout.setContentsMargins(border, border, border, border)
        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        self.key_press_handler.handle_key_press(event)

    def populate_list(self):
        for subdir in sorted(os.listdir(self.directory)):
            full_path = os.path.join(self.directory, subdir)
            if os.path.isdir(full_path):
                item = QListWidgetItem(subdir)
                self.list_widget.addItem(item)
    
    def scroll_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)

    def select_item(self):
        item = self.list_widget.currentItem()
        if item:
            print(f"Selected item: {item.text()}")
            filepath = item.text()
            reader = EpubReader(filepath=filepath, width=width, height=height, border=border)
            reader.show()

    def scroll_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            self.list_widget.setCurrentRow(current_row + 1)

app = QApplication(sys.argv)
width = 600
height = 800
border = 5

directory_selector = BookSelector('epubs_parsed', width=width, height=height, border=border)
directory_selector.show()

sys.exit(app.exec())
