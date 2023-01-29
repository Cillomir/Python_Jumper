import math
import time
import pygame as pg
import settings as stt

# *****~~~~****~~~***~~**~ DEFINE COLORS (16-bit, 5-gray)  ~**~~***~~~****~~~~*****
White, Black = (255, 255, 255), (0, 0, 0)
Gray1, Gray2, Gray3 = (180, 180, 180), (125, 125, 125), (70, 70, 70)
Red1, Red2 = (255, 0, 0), (125, 0, 0)
Orange1, Orange2 = (255, 140, 0), (125, 60, 0)
Yellow1, Yellow2 = (255, 255, 0), (130, 120, 0)
Green1, Green2 = (0, 255, 0), (0, 125, 0)
Cyan1, Cyan2 = (0, 255, 255), (0, 125, 125)
Blue1, Blue2 = (50, 50, 255), (0, 0, 140)
Purple1, Purple2 = (240, 0, 240), (125, 0, 125)
Pink1, Pink2 = (255, 125, 200), (130, 60, 100)

# *****~~~~****~~~***~~**~ INITIALIZE PYGAME MODULE   ~**~~***~~~****~~~~*****
pg.init()
clock = pg.time.Clock()
mouse_x, mouse_y = pg.mouse.get_pos()

# ***---***---***-- DEFINE SCREEN & SYSTEM SETTINGS --***---***---***
screen = pg.display.set_mode((0, 0))
screen_x = 1920
# pygame.display.Info().current_w #1920
screen_y = 1020
# pygame.display.Info().current_h #1020
screen_tiles = math.ceil(screen_x / 100)
FPS = 20
font_size = [0,
             int(screen_x / 60),
             int(screen_x / 40),
             int(screen_x / 25),
             int(screen_x / 16),
             int(screen_x / 16)]


# ***---***---***-- DEFINE PRINT FUNCTION --***---***---***
def _print(font, text, color, pos_x, pos_y):
    if font not in range(1, len(font_size)):
        font = 2
    font_type = pg.font.SysFont(None, font_size[font])
    font_text = font_type.render(text, True, color)
    if pos_x == "center":
        text_x = pg.font.Font.size(font_type, text)[0]
        pos_x = (screen_x - text_x) / 2
    if pos_y == "center":
        text_y = pg.font.Font.size(font_type, text)[1]
        pos_y = (screen_y - text_y) / 2
    screen.blit(font_text, (pos_x, pos_y))


# ***---***---***-- DEFINE CLOCK FUNCTION --***---***---***
class CurrentTime:
    """ Print a real-time clock to the display """
    def __init__(self):
        now = time.localtime(time.time())
        hour = now.tm_hour
        if hour > 12:
            hour -= 12
        hour = str(hour)
        minute = str(now.tm_min).zfill(2)
        second = str(now.tm_sec).zfill(2)
        _print(2, f"{hour}:{minute}:{second}", Black, screen_x - 160, 20)


# ***---***---***-- DEFINE BUTTON FUNCTION --***---***---***
class Button:
    def __init__(self):
        pass
        #self.render = self.font = self.text = self.pad_x = self.pad_y = self.click = None
        #self.width = self.height = self.color = self.color2 = self.border = self.border_c = None

    def text(self, font, text, color, pad_x=0, pad_y=0):
        font_type = pg.font.SysFont(None, font_size[font])
        self.render = font_type.render(text, True, color)
        self.font = font_type
        self.text = text
        self.pad_x = pad_x
        self.pad_y = pad_y

    def box(self, color, color2, width=0, height=0, border=0, border_c=Black):
        if width == 0:
            width = pg.font.Font.size(self.font, self.text)[0]
        if height == 0:
            height = pg.font.Font.size(self.font, self.text)[1]
        if color2 == "same":
            color2 = color
        self.width = width
        self.height = height
        self.color = color
        self.color2 = color2
        self.border = border
        self.border_c = border_c

    def draw(self, pos_x, pos_y):
        pos_x2 = pos_x + self.width
        pos_y2 = pos_y + self.height
        if pos_x <= mouse_x <= pos_x2 and pos_y <= mouse_y <= pos_y2:
            self.click = True
            color = self.color2
        else:
            self.click = False
            color = self.color
        if self.pad_x == "center":
            pad_x = pg.font.Font.size(self.font, self.text)[0]
            pad_x = (self.width - pad_x) / 2
        else:
            pad_x = self.pad_x
        if self.pad_y == "center":
            pad_y = pg.font.Font.size(self.font, self.text)[1]
            pad_y = (self.height - pad_y) / 2
        else:
            pad_y = self.pad_y
        pos = (pos_x, pos_y, self.width, self.height)
        pos_b = (pos_x - self.border, pos_y - self.border,
                 self.width + (self.border * 2), self.height + (self.border * 2))
        pos_t = (pos_x + pad_x, pos_y + pad_y)
        pg.draw.rect(screen, self.border_c, pos_b)
        pg.draw.rect(screen, color, pos)
        screen.blit(self.render, pos_t)
