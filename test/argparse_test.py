import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Read a book.')

# Add the arguments
parser.add_argument('-b', '--book',
                    type=str,
                    help='The name of the book to read')

# Parse the arguments
args = parser.parse_args()

# Now you can use args.book to get the book title
print(f'Reading book: {args.book}')
