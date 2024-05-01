import os
from PIL import Image,ImageDraw,ImageFont
from utils import *

class EBookReader:
    def __init__(self, epd):
        self.VERTICAL = False
        self.MARGINS = 0
        self.FONT_SIZE = 25
        self.PARAGRAPH_SPACE = 5
        self.BUTTOM_BCM = 26
        self.DEBOUNCE_PERIOD = 0.3
        self.picdir = os.path.join("waveshare_lib/pic")
        self.FONT = ImageFont.truetype(os.path.join(self.picdir, "arial.ttf"), self.FONT_SIZE)
        self.index = 0
        self.old_index = 0
        self.extra_lines = ""
        self.filepath = ""
        self.book = ""
        self.width = 0
        self.height = 0
        self.contents = {}
        self.epd = epd

    def store_content(self):
        for i in os.listdir(self.filepath):
            full_path = os.path.join(self.filepath, i)
            if os.path.isfile(full_path):
                with open(full_path, "r") as file:
                        self.contents[i] = file.read()

    def get_content(self, i):
        content = self.contents.get(f"{i}.txt")
        if content is None:
            content = "E N D O F C O N T E N T " * 50
            print(f"File {i} not found, returning default content")
        else:
            print(f"Opening file {i}")
        return content
        
    def button_pressed_animation(self, ScreenImage, text):
        self.epd.init_fast()
        draw = ImageDraw.Draw(ScreenImage)
        text_length = draw.textlength(text, font=self.FONT)
        left, top, right, bottom = self.width-text_length, self.height-self.FONT_SIZE, self.width, self.height
        draw.rectangle((left, top, right, bottom), fill=255)
        draw.text((left, top), text, font=self.FONT, fill=0)
        self.epd.display_Partial(self.epd.getbuffer(ScreenImage), 0, 0, self.width, self.height)

    def show_next_screen(self, epd, overflow_lines=""):
        self.old_index = self.index
        x_cursor = self.MARGINS
        y_cursor = self.MARGINS

        epd.init_fast()
        ScreenImage = Image.new("1", (self.width, self.height), 255)
        screen_buffer = ImageDraw.Draw(ScreenImage)
        text_height = self.height - 2 * self.MARGINS - self.FONT_SIZE
        extra_lines = []

        if overflow_lines:
            for _, line in enumerate(overflow_lines):
                if y_cursor > text_height - self.FONT_SIZE:
                    extra_lines.append(line)
                else:
                    # print(line)
                    screen_buffer.text((x_cursor,y_cursor), line, font=self.FONT, fill=0)
                    y_cursor += self.FONT_SIZE

        while y_cursor <= text_height - self.FONT_SIZE:
            y_cursor += self.PARAGRAPH_SPACE
            content = self.get_content(self.index)
            lines = fit_text_within_screen(content, self.FONT, self.MARGINS, self.width, self.FONT_SIZE, self.filepath)
            for _, line in enumerate(lines):
                if y_cursor > text_height - self.FONT_SIZE:
                    extra_lines.append(line)
                else:
                    # print(line)
                    screen_buffer.text((x_cursor,y_cursor), line, font=self.FONT, fill=0)
                    y_cursor += self.FONT_SIZE
            self.index += 1

        save_index(self.filepath, self.old_index)

        # Progress bar
        lst = os.listdir(self.filepath)
        n_files = len(lst) - 1
        progress = f"Page {self.old_index}/{n_files} - {str(round(100 * self.old_index/n_files, 2))} %"
        progress_width = self.width * self.old_index / n_files
        font_small = ImageFont.truetype(os.path.join(self.picdir, "arial.ttf"), self.FONT_SIZE-5)
        screen_buffer.rectangle((0, self.height-4, progress_width, self.height), fill=0)
        screen_buffer.text((round(self.MARGINS/2), self.height-self.FONT_SIZE-round(self.MARGINS/2)), progress, font=font_small, fill=0)

        # Update screen
        epd.display(epd.getbuffer(ScreenImage))
        sleep_epd(epd)
        return extra_lines, ScreenImage

    def show_previous_screen(self, epd):
        self.index = self.old_index - 1
        if self.index <= 0:
            self.index = 1
        return self.show_next_screen(epd)
