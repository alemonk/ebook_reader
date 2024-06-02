import os
from PIL import Image,ImageDraw,ImageFont
from utils import *
import time

class EBookReader:
    def __init__(self, epd):
        # Parameters
        self.VERTICAL = False
        self.FAST_MODE = False
        self.PROGRESS_BAR = True
        self.MARGINS = 0
        self.FONT_SIZE = 25
        self.PARAGRAPH_SPACE = 5
        self.SWITCH_GPIO = 26
        self.SCREENSAVER_QUOTES = False

        self.picdir = os.path.join('waveshare_lib/pic')
        self.FONT = ImageFont.truetype(os.path.join(self.picdir, 'arial.ttf'), self.FONT_SIZE)
        # self.FONT = ImageFont.truetype(os.path.join(self.picdir, 'RobotoMono-Regular.ttf'), self.FONT_SIZE)
        # self.FONT = ImageFont.truetype(os.path.join(self.picdir, 'RobotoMono-Medium.ttf'), self.FONT_SIZE)
        self.font_small = ImageFont.truetype(os.path.join(self.picdir, 'arial.ttf'), self.FONT_SIZE-5)
        self.index = 0
        self.old_index = 0
        self.old_page_index = 0
        self.filepath = ''
        self.book = ''
        self.width = 0
        self.height = 0
        self.contents = {}
        self.epd = epd
        self.extra_lines = []
        self.last_switch_state = False
        self.last_switch_toggle_time = time.time()
        self.screen_buffer = None
        self.ScreenImage = None

    def set_last_switch_state(self, state):
        self.last_switch_state = state

    def store_content(self):
        for i in os.listdir(self.filepath):
            full_path = os.path.join(self.filepath, i)
            if os.path.isfile(full_path):
                with open(full_path, 'r') as file:
                    self.contents[i] = file.read()

    def get_content(self, i):
        content = self.contents.get(f'{i}.txt')
        if content is None:
            content = 'E N D O F C O N T E N T ' * 50
            print(f'File {i} not found, returning default content')
        else:
            print(f'Opening file {i}')
        return content

    def button_pressed_animation(self, ScreenImage, text):
        self.epd.init_fast()
        draw = ImageDraw.Draw(ScreenImage)
        text_length = draw.textlength(text, font=self.FONT)
        left, top, right, bottom = self.width-text_length, self.height-self.FONT_SIZE, self.width, self.height
        draw.rectangle((left, top, right, bottom), fill=255)
        draw.text((left, top), text, font=self.font_small, fill=0)
        self.epd.display_Partial(self.epd.getbuffer(ScreenImage), 0, 0, self.width, self.height)

    def load_next_screen(self):
        self.old_page_index = self.old_index
        self.old_index = self.index
        x_cursor = self.MARGINS
        y_cursor = self.MARGINS

        self.ScreenImage = Image.new('1', (self.width, self.height), 255)
        self.screen_buffer = ImageDraw.Draw(self.ScreenImage)
        text_height = self.height - 2 * self.MARGINS - self.FONT_SIZE
        overflow_lines = self.extra_lines
        self.extra_lines = []

        if overflow_lines:
            for _, line in enumerate(overflow_lines):
                if y_cursor > text_height - self.FONT_SIZE:
                    self.extra_lines.append(line)
                else:
                    # print(line)
                    self.screen_buffer.text((x_cursor,y_cursor), line, font=self.FONT, fill=0)
                    y_cursor += self.FONT_SIZE + self.PARAGRAPH_SPACE
            y_cursor += self.PARAGRAPH_SPACE

        while y_cursor <= text_height - self.FONT_SIZE:
            content = self.get_content(self.index)
            lines = fit_text_within_screen(text=content,
                                           font=self.FONT,
                                           margins=self.MARGINS,
                                           width=self.width,
                                           font_size=self.FONT_SIZE,
                                           filepath=self.filepath,
                                           fast_mode=self.FAST_MODE)
            for _, line in enumerate(lines):
                if y_cursor > text_height - self.FONT_SIZE:
                    self.extra_lines.append(line)
                else:
                    # print(line)
                    self.screen_buffer.text((x_cursor,y_cursor), line, font=self.FONT, fill=0)
                    y_cursor += self.FONT_SIZE + self.PARAGRAPH_SPACE
            y_cursor += self.PARAGRAPH_SPACE + self.PARAGRAPH_SPACE
            self.index += 1

            paragraphs_left, _ = get_closest_heading(index=self.index, filepath=self.filepath)
            if paragraphs_left == 0:
                y_cursor = self.height

        if self.PROGRESS_BAR:
            paragraphs_left, next_paragraph = get_closest_heading(index=self.index, filepath=self.filepath)
            
            lst = os.listdir(self.filepath)
            n_files = len(lst) - 1
            progress = f'Page {self.old_index}/{n_files} - {str(round(100 * self.old_index/n_files, 2))} % - {paragraphs_left} until {next_paragraph}'
            progress_width = self.width * self.old_index / n_files
            self.screen_buffer.line((0,self.height-self.FONT_SIZE-round(self.MARGINS), self.width, self.height-self.FONT_SIZE-round(self.MARGINS)),fill=0)
            self.screen_buffer.line((0,self.height-1, self.width, self.height-1),fill=0)
            self.screen_buffer.rectangle((0, self.height-4, progress_width, self.height), fill=0)
            self.screen_buffer.text((round(self.MARGINS), self.height-self.FONT_SIZE-round(self.MARGINS)), progress, font=self.font_small, fill=0)

        save_index(self.filepath, self.old_page_index)
        print('Page loaded!')

    def update_screen(self, epd):
        epd.init_fast()
        epd.display(epd.getbuffer(self.ScreenImage))
        sleep_epd(epd)
        print('Screen Updated!')

    def load_previous_screen(self):
        self.extra_lines = []
        self.index = self.old_page_index - 2
        if self.index <= 0:
            self.index = 1
        self.load_next_screen()
