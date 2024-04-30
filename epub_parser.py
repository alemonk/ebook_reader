import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from utils import *

try:
    BOOK = get_book_name()
    FILEPATH = epub.read_epub(f"epubs/{BOOK}.epub")
    os.makedirs(f"parsed_epubs/{BOOK}", exist_ok=True)

    counter = 1

    for item in FILEPATH.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parse the content of the item
            soup = BeautifulSoup(item.get_content(), "html.parser")

            # Loop through each <p> element in the content
            for p in soup.find_all("p"):
                # Get the class of the <p> element
                p_class = p.get("class")[0] if p.get("class") else "NoClass"

                # Handle <br/> tags
                for br in p.find_all("br"):
                    # br.replace_with("__newline__ ")
                    br.replace_with("\n")

                # Write the class and the content of the <p> element to a text file
                with open(f"parsed_epubs/{BOOK}/{counter}.txt", "w") as f:
                #    f.write(f"Class: {p_class}\n\n")
                    f.write(p.text)

                counter += 1
except Exception as e:
    print(f"Error: {e}")
    error_screen(e)
