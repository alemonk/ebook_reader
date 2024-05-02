import os
from PIL import ImageFont

def average_font_width(font_name, font_size, characters):
    font = ImageFont.truetype(os.path.join(picdir, font_name), font_size)

    width = font.getlength(characters)

    return width / len(characters)

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
picdir = os.path.join(parent_dir + "/ebook_reader/waveshare_lib/pic")
size = 25

characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
avg_width = average_font_width('RobotoMono-ExtraLight.ttf', size, characters)
print(f'The average font width is {avg_width}')

characters = 'a'
avg_width = average_font_width('RobotoMono-ExtraLight.ttf', size, characters)
print(f'The average font width is {avg_width}')

characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
avg_width = average_font_width('arial.ttf', size, characters)
print(f'The average font width is {avg_width}')

characters = 'a'
avg_width = average_font_width('arial.ttf', size, characters)
print(f'The average font width is {avg_width}')
