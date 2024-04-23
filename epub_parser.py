import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Read the EPUB file
book_name = '1984'
book = epub.read_epub(f'epubs/{book_name}.epub')

# Create a directory for the text files
os.makedirs(f'parsed_epubs/{book_name}', exist_ok=True)

# Initialize a counter for the text files
counter = 1

# Loop through each item in the book
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        # Parse the content of the item
        soup = BeautifulSoup(item.get_content(), 'html.parser')

        # Loop through each <p> element in the content
        for p in soup.find_all('p'):
            # Get the class of the <p> element
            p_class = p.get('class')[0] if p.get('class') else 'NoClass'

            # Handle <br/> tags
            for br in p.find_all('br'):
                br.replace_with('__newline__ ')

            # Write the class and the content of the <p> element to a text file
            with open(f'parsed_epubs/{book_name}/{counter}.txt', 'w') as f:
            #    f.write(f'Class: {p_class}\n\n')
               f.write(p.text)

            # Increment the counter
            counter += 1
