import os

directory = "parsed_epubs/1984"
lst = os.listdir(directory) # your directory path
number_files = len(lst)
print(number_files)
