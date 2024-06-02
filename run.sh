#!/bin/bash

# SELECT BOOK HERE
BOOK="1984"
FILEPATH="parsed_epubs/${BOOK}"

# Move to main branch
git fetch origin
git reset --hard origin/main
# source pyenv/bin/activate

# Parse selected book
if [ ! -d "$FILEPATH" ]; then
	echo "Parsing $BOOK..."
	python3 epub_parser.py --book $BOOK
fi
echo "Opening $BOOK... enjoy!"
python3 read_book.py --book $BOOK

# deactivate
