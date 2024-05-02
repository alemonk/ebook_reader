import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import json
from utils import *

try:
    BOOK = get_book_name()
    # BOOK = "1984"
    FILEPATH = epub.read_epub(f"epubs/{BOOK}.epub")
    base_dir = f"parsed_epubs/{BOOK}"
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "meta"), exist_ok=True)

    counter = 1
    headings = {}

    for item in FILEPATH.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")

            # Remove all <a> elements
            for a in soup.find_all("a"):
                a.decompose()

            for p in soup.find_all("p"):
                p_class = p.get("class")[0] if p.get("class") else "NoClass"

                for br in p.find_all("br"):
                    br.replace_with("\n")

                if p_class in ["Heading-1", "Heading-2", "h1", "h2"]:
                    headings[counter] = {"class": p_class, "text": p.text.strip()}

                with open(f"parsed_epubs/{BOOK}/{counter}.txt", "w") as f:
                    f.write(p.text)

                counter += 1

    with open(f"parsed_epubs/{BOOK}/meta/headings.json", "w") as f:
        json.dump(headings, f, indent=4)

except Exception as e:
    print(f"Error: {e}")
