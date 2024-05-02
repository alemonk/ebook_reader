import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def epub_to_txt(epub_path, txt_path):
    book = epub.read_epub(epub_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                txt_file.write(soup.prettify())
import os

def print_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            print(filename)

current_directory = os.path.dirname(os.path.realpath(__file__))
print_files_in_directory(current_directory)
epub_to_txt(current_directory+'/verne_ventimila_leghe_sotto_ai_mari.epub', 'verne_ventimila_leghe_sotto_ai_mari.txt')
