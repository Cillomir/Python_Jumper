# Program: Jumper
#   A simple interactive game showing movement control, basic animations, and collisions
# Requires: pygame library
# Created by: Joel Leckie
# May 2021 - Initial file creation
# July 2021 - v. 1 complete
# January 2023 - Additional refinements

    # Planned Additions:
# Start Menu: Start Game, High Scores, Quit Game
# Main Game Screen: Choose player color (Red, Blue, Green)
#   - arrow to select, color in-between, player preview, default red
# High Score Screen (Top 10 points)
# Moving background, scrolling foreground (grass, trees, ledges)
# Varying 5, 6, 8, 10 points per goober
# Time elapsed on game screen
# Enter name for High Score (up to 8 characters)
# Quit Menu: Yes, No

import pygame
from pygame.locals import (K_a, K_s, K_d, K_w,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_RETURN, K_ESCAPE,
    KEYDOWN, MOUSEBUTTONDOWN)
import time
#import datetime
import random
import math

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
pygame.init()

# ***---***---***-- DEFINE SCREEN & SYSTEM SETTINGS --***---***---***
screen = pygame.display.set_mode((0, 0))
screen_x = 1920
# pygame.display.Info().current_w #1920
screen_y = 1020
# pygame.display.Info().current_h #1020
screen_tiles = math.ceil(screen_x / 100)
clock = pygame.time.Clock()
FPS = 20

# ***---***---***-- DEFINE PRINT FUNCTION --***---***---***
font_size = [0, int(screen_x / 60), int(screen_x / 40),
             int(screen_x / 25), int(screen_x / 16), int(screen_x / 16)]


def Print(font, text, color, pos_x, pos_y):
    if font not in range(1, 6):
        font = 2
    font_type = pygame.font.SysFont(None, font_size[font])
    font_text = font_type.render(text, True, color)
    text_x = pygame.font.Font.size(font_type, text)[0]
    text_y = pygame.font.Font.size(font_type, text)[1]
    if pos_x == "center":
        pos_x = (screen_x - text_x) / 2
    if pos_y == "center":
        pos_y = (screen_y - text_y) / 2
    screen.blit(font_text, (pos_x, pos_y))


# ***---***---***-- DEFINE CLOCK FUNCTION --***---***---***
class Current_Time:
    def __init__(self):
        Passed = time.time()
        Now = time.localtime(Passed)
        Hour = Now.tm_hour
        if Hour > 12:
            Hour -= 12
        Hour = str(Hour)
        Minute = str(Now.tm_min).zfill(2)
        Second = str(Now.tm_sec).zfill(2)
        Print(2, Hour + ":" + Minute + ":" + Second, Black, screen_x - 160, 20)


# ***---***---***-- DEFINE BUTTON FUNCTION --***---***---***
class Button:
    def __init__(self):
        pass

    def text(self, font, text, color, pad_x=0, pad_y=0):
        font_type = pygame.font.SysFont(None, font_size[font])
        self.render = font_type.render(text, True, color)
        self.font = font_type
        self.text = text
        self.pad_x = pad_x
        self.pad_y = pad_y

    def box(self, color, color2, width=0, height=0, border=0, border_c=Black):
        if width == 0:
            width = pygame.font.Font.size(self.font, self.text)[0]
        if height == 0:
            height = pygame.font.Font.size(self.font, self.text)[1]
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
            pad_x = pygame.font.Font.size(self.font, self.text)[0]
            pad_x = (self.width - pad_x) / 2
        else:
            pad_x = self.pad_x
        if self.pad_y == "center":
            pad_y = pygame.font.Font.size(self.font, self.text)[1]
            pad_y = (self.height - pad_y) / 2
        else:
            pad_y = self.pad_y
        POS = (pos_x, pos_y, self.width, self.height)
        POS_B = (pos_x - self.border, pos_y - self.border,
                 self.width + (self.border * 2), self.height + (self.border * 2))
        POS_T = (pos_x + pad_x, pos_y + pad_y)
        pygame.draw.rect(screen, self.border_c, POS_B)
        pygame.draw.rect(screen, color, POS)
        screen.blit(self.render, POS_T)


# *****~~~~****~~~***~~**~ INITIATE GAME VARIABLES   ~**~~***~~~****~~~~*****
start_menu_on = True
main_game_on = False
player_dead = False
Pause = False
Players = 1
P_Colors = ["Red", "Green", "Blue", "Cyan", "Orange", "Purple", "???"]
P_Images = ["PlayerRed.png", "PlayerGreen.png", "PlayerBlue.png",
            "PlayerCyan.png", "PlayerOrange.png", "PlayerPurple.png", "PlayerNinja.png"]
P_Options = len(P_Images) - 1
P1_Select = 0
P2_Select = 1
P1_Score = 0
P2_Score = 0
Passing = 10
walk = 6
jump = 38
gravity = 2.7

# *****~~~~****~~~***~~**~ DEFINE THE GAME SOUNDS ~**~~***~~~****~~~~*****
main_music = pygame.mixer.Sound("SFX/levelmusic.wav")
main_music.set_volume(0.55)
sfx_jump = pygame.mixer.Sound("SFX/quickjump.wav")
sfx_jump.set_volume(0.9)
sfx_hit_head = pygame.mixer.Sound("SFX/blockhit.wav")
sfx_hit_head.set_volume(0.85)
sfx_dead = pygame.mixer.Sound("SFX/playerlosing.wav")
sfx_dead.set_volume(0.90)
sfx_goober_kill = pygame.mixer.Sound("SFX/retrosquish.wav")
sfx_goober_kill.set_volume(0.9)

# *****~~~~****~~~***~~**~ DEFINE THE GAME SPRITES ~**~~***~~~****~~~~*****
all_sprites = pygame.sprite.Group()
all_ground = pygame.sprite.Group()

# *****----*****----*****--- DEFINE THE GAME DISPLAY ---*****----*****----*****
bd_sky = pygame.image.load("Backdrops/Sky.png").convert()  # 500x600
bd_grass = pygame.image.load("Backdrops/Grass.png").convert()  # 500x300


def backdrop_draw():
    screen.fill(Cyan1)
    for x in range(4):
        screen.blit(bd_sky, (x * 500 - 25, 200))
        screen.blit(bd_grass, (x * 500 - 25, 800))
    Print(4, "Jump on the", Black, "center", 20)
    Print(4, "Goobers", Black, "center", 110)
    Print(2, "Player1 Score: " + str(P1_Score), Black, 50, 45)
    Print(2, "Lives: ", Black, 375, 45)
    if player1.lives >= 1:
        screen.blit(player1.image_mini, (485, 40))
    if player1.lives >= 2:
        screen.blit(player1.image_mini, (510, 40))
    if player1.lives >= 3:
        screen.blit(player1.image_mini, (535, 40))
    if Players == 2:
        Print(2, "Player2 Score: " + str(P2_Score), Black, 50, 105)
        Print(2, "Lives: ", Black, 375, 105)
        if player2.lives >= 1:
            screen.blit(player2.image_mini, (485, 100))
        if player2.lives >= 2:
            screen.blit(player2.image_mini, (510, 100))
        if player2.lives >= 3:
            screen.blit(player2.image_mini, (535, 100))


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        if image == "clear":
            self.image = pygame.Surface([screen_x, screen_y - 800])
            self.image.fill(White)
            self.image.set_colorkey(White)
        else:
            self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        all_sprites.add(self)
        all_ground.add(self)


def Ground_Generate():
    ground1 = Platform("clear", 0, 800)
    platform1 = Platform("Foreground/block8.png", 350, 650)
    platform2 = Platform("Foreground/block7.png", 900, 650)
    platform3 = Platform("Foreground/block10.png", 1400, 650)
    respawn = Platform("Foreground/block4d.png", 25, 300)


all_players = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        self.movex = 0
        self.movey = 0
        self.lives = 3
        self.grounded = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        mini_w = int(self.rect.width / 2)
        mini_h = int(self.rect.height / 2)
        self.image_mini = pygame.transform.scale(self.image, (mini_w, mini_h))
        self.rect.bottom = 800
        all_sprites.add(self)
        all_players.add(self)

    def update(self):
        # ****---***---**--- ACTIVATE GRAVITY & MOVEMENT ---**---***---****
        self.movey += gravity
        self.rect.x += self.movex
        self.rect.y += self.movey
        if self.rect.left <= 20:
            self.rect.left = 25
        if self.rect.right >= screen_x - 20:
            self.rect.right = screen_x - 25
        if self.movex > 0:
            self.image = self.image_r
        elif self.movex < 0:
            self.image = self.image_l
        # ****---***---**--- COLLISION TEST AGAINST PLATFORMS ---**---***---****
        platform_hit = pygame.sprite.spritecollide(self, all_ground, False)
        for g in platform_hit:
            # Hit your head on a platform
            if self.movey < 0 and g.rect.left - 5 < self.rect.centerx < g.rect.right + 5:
                self.movey = gravity
                self.rect.top = g.rect.bottom
                sfx_hit_head.play()
            # Landing atop a platform
            elif self.movey > 0 and g.rect.left - 5 < self.rect.centerx < g.rect.right + 5:
                self.movey = 0
                self.rect.bottom = g.rect.top
                self.grounded = True
            # Hit the left side of a platform
            elif self.rect.left < g.rect.left:
                if self.movex > 0:
                    self.movex = 0
                self.rect.right = g.rect.left - walk
            # Hit the right side of a platform
            elif self.rect.right > g.rect.right:
                if self.movex < 0:
                    self.movex = 0
                self.rect.left = g.rect.right + walk


# *****----*****----*****--- DEFINE THE GOOBERS ---*****----*****----*****
all_goobers = pygame.sprite.Group()


class Goober(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(screen_x, 750))
        self.speed = speed
        self.movey = 0
        if self.speed == 11:
            self.rect.y = 500
        self.Dead = False
        self.dead = int(FPS * 1.25)
        all_sprites.add(self)
        all_goobers.add(self)
        global Passing
        Passing = 0

    def update(self):
        global P1_Score
        global P2_Score
        global Passing
        self.movey += gravity
        self.rect.x -= self.speed
        self.rect.y += self.movey
        if self.Dead:
            sfx_goober_kill.play()
            self.dead -= 1
            if self.dead % 6 >= 3:
                self.image = pygame.image.load("Sprites/GooberCrushed1.png").convert_alpha()
            if self.dead % 6 <= 2:
                self.image = pygame.image.load("Sprites/GooberCrushed2.png").convert_alpha()
            self.rect.y += 25
            if self.dead > 0 and self.speed == 6:
                Print(2, "+1", Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 8:
                Print(2, "+1", Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 9:
                Print(2, "+2", Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 10:
                Print(2, "+2", Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 12:
                Print(2, "+3", Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 11:
                Print(2, "+3", Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead == 0:
                pygame.sprite.Sprite.kill(self)
        # ****---***---**--- CHECK FOR A PLAYER COLLISION ---**---***---****
        if pygame.sprite.collide_rect(self, player1) and not self.Dead:
            if player1.movey > 0 and not player1.grounded:
                if self.speed == 6:
                    P1_Score += 1
                if self.speed == 8:
                    P1_Score += 1
                if self.speed == 9:
                    P1_Score += 2
                if self.speed == 10:
                    P1_Score += 2
                if self.speed == 12:
                    P1_Score += 3
                if self.speed == 11:
                    P1_Score += 3
                self.Dead = True
                player1.rect.y -= 5
            else:
                player1.lives -= 1
                player1.rect.x = 75
                player1.rect.y = 225
                player1.movex = 0
                sfx_dead.play()
                if Players == 1:
                    Passing = 20
                    for x in all_goobers:
                        x.kill()
                    return
        if pygame.sprite.collide_rect(self, player2) and not self.dead:
            if player2.movey > 0 and not player2.grounded:
                if self.speed == 6:
                    P2_Score += 1
                if self.speed == 8:
                    P2_Score += 1
                if self.speed == 9:
                    P2_Score += 2
                if self.speed == 10:
                    P2_Score += 2
                if self.speed == 12:
                    P2_Score += 3
                if self.speed == 11:
                    P2_Score += 3
                self.Dead = True
                player2.rect.y -= 5
            else:
                player2.lives -= 1
                player2.rect.x = 50
                player2.rect.y = 225
                player2.movex = 0
                sfx_dead.play()
        # ****---***---**--- CHECK FOR GROUND & PLATFORM ---**---***---****
        ground_land = pygame.sprite.spritecollide(self, all_ground, False)
        for g in ground_land:
            # Hit its head on a platform
            if self.movey < 0:
                self.movey = gravity
                self.rect.top = g.rect.bottom
            # Hit the side of a platform
            elif self.rect.left > g.rect.right - self.speed:
                self.movey = gravity
                self.rect.left = g.rect.right + 5
            # Landing atop a platform
            elif self.movey > 0:
                self.movey = 0
                self.rect.bottom = g.rect.top
                if self.speed == 9 and self.movey >= 0 and random.randrange(0, 10) == 1:
                    self.movey = -38
                if self.speed == 12 and self.movey >= 0 and random.randrange(0, 8) == 1:
                    self.movey = -45
        if self.speed == 11 and self.rect.y <= 400:
            self.movey += 5
        if self.speed == 11 and self.rect.y >= 575:
            self.movey -= 15
        if self.rect.right <= 0:
            pygame.sprite.Sprite.kill(self)
            Passing += 5


# ****---***---**--- GOOBER CREATION via SCORE ---**---***---****
def Make_Goober():
    spawn = random.randrange(1, 100)
    G_Brown = "Sprites/GooberBrown.png"
    G_Green = "Sprites/GooberGreen.png"
    G_Blue = "Sprites/GooberBlue.png"
    G_Red = "Sprites/GooberRed.png"
    G_Black = "Sprites/GooberBlack.png"
    G_White = "Sprites/GooberWhite.png"
    # Score under 10
    if (P1_Score + P2_Score) <= 10:
        if Passing >= 35 and spawn >= 80:
            Goober(G_Brown, 6)
    # Score under 15
    elif 10 < (P1_Score + P2_Score) <= 15:
        if Passing >= 35 and spawn >= 85:
            Goober(G_Brown, 6)
        elif Passing >= 40 and spawn >= 75:
            Goober(G_Green, 8)
    # Score under 20
    elif 15 < (P1_Score + P2_Score) <= 20:
        if Passing >= 35 and spawn >= 86:
            Goober(G_Brown, 6)
        elif Passing >= 40 and spawn >= 78:
            Goober(G_Green, 8)
        elif Passing >= 45 and spawn >= 65:
            Goober(G_Blue, 9)
    # Score under 25
    elif 20 < (P1_Score + P2_Score) <= 25:
        if Passing >= 32 and spawn >= 90:
            Goober(G_Brown, 6)
        elif Passing >= 35 and spawn >= 80:
            Goober(G_Green, 8)
        elif Passing >= 40 and spawn >= 72:
            Goober(G_Blue, 9)
        elif Passing >= 45 and spawn >= 60:
            Goober(G_Red, 10)
    # Score under 30
    elif 25 < (P1_Score + P2_Score) <= 30:
        if Passing >= 32 and spawn >= 92:
            Goober(G_Brown, 6)
        elif Passing >= 36 and spawn >= 84:
            Goober(G_Green, 8)
        elif Passing >= 40 and spawn >= 78:
            Goober(G_Blue, 9)
        elif Passing >= 44 and spawn >= 70:
            Goober(G_Red, 10)
        elif Passing >= 48 and spawn >= 60:
            Goober(G_Black, 12)
    # Score under 35
    elif 30 < (P1_Score + P2_Score) <= 35:
        if Passing >= 32 and spawn >= 92:
            Goober(G_Brown, 6)
        elif Passing >= 34 and spawn >= 84:
            Goober(G_Green, 8)
        elif Passing >= 36 and spawn >= 78:
            Goober(G_Blue, 9)
        elif Passing >= 38 and spawn >= 70:
            Goober(G_Red, 10)
        elif Passing >= 40 and spawn >= 60:
            Goober(G_Black, 12)
    # Score under 40
    elif 35 < (P1_Score + P2_Score) <= 40:
        if Passing >= 30 and spawn >= 95:
            Goober(G_Brown, 6)
        elif Passing >= 33 and spawn >= 88:
            Goober(G_Green, 8)
        elif Passing >= 36 and spawn >= 82:
            Goober(G_Blue, 9)
        elif Passing >= 39 and spawn >= 75:
            Goober(G_Red, 10)
        elif Passing >= 42 and spawn >= 65:
            Goober(G_Black, 12)
        elif Passing >= 46 and spawn >= 60:
            Goober(G_White, 11)
    # Score over 40
    elif (P1_Score + P2_Score) > 40:
        if Passing >= 28 and spawn >= 96:
            Goober(G_Brown, 6)
        elif Passing >= 30 and spawn >= 92:
            Goober(G_Green, 8)
        elif Passing >= 32 and spawn >= 88:
            Goober(G_Blue, 9)
        elif Passing >= 34 and spawn >= 80:
            Goober(G_Red, 10)
        elif Passing >= 37 and spawn >= 72:
            Goober(G_Black, 12)
        elif Passing >= 40 and spawn >= 64:
            Goober(G_White, 11)


# *****~~~~****~~~***~~**~ START MENU DISPLAY ~**~~***~~~****~~~~*****

# ***---***---***-- DEFINE THE START MENU --***---***---***
start_true = Button()
player_numbers = Button()
p_number = Button()
start_false = Button()
P1_color = Button()
P1_color_left = Button()
P1_color_right = Button()
P2_color = Button()
P2_color_left = Button()
P2_color_right = Button()

start_true.text(4, "Start Game", Black, "center", "center")
player_numbers.text(4, "Players: ", Black, "center", "center")
p_number.text(4, "  ", Black, "center", "center")
start_false.text(4, "Quit Game", Black, "center", "center")
P1_color.text(4, " ", Black, "center", "center")
P1_color_left.text(4, "<-", Black, "center", "center")
P1_color_right.text(4, "->", Black, "center", "center")
P2_color.text(4, " ", Black, "center", "center")
P2_color_left.text(4, "<-", Black, "center", "center")
P2_color_right.text(4, "->", Black, "center", "center")

start_true.box(Blue1, Green1, 500, 95, 5, Black)
player_numbers.box(Blue1, "same", 400, 95, 5, Black)
p_number.box(Cyan2, Green1, 80, 85, 5, Purple2)
start_false.box(Blue1, Green1, 500, 95, 5, Black)
P1_color.box(Blue1, "same", 400, 95, 5, Black)
P1_color_left.box(Blue1, Green1, 75, 85, 5, Black)
P1_color_right.box(Blue1, Green1, 75, 85, 5, Black)
P2_color.box(Blue1, "same", 400, 95, 5, Black)
P2_color_left.box(Blue1, Green1, 75, 85, 5, Black)
P2_color_right.box(Blue1, Green1, 75, 85, 5, Black)

# Define a high score table, open a saved table from file
"""
high_score = {}
high_score[0] = "name1: ".ljust(16,"~") + str(110)
high_score[1] = "name1: ".ljust(16, "~") + str(100)
high_score[2] = "name1: ".ljust(16, "~") + str(80)
high_score[3] = "name1: ".ljust(16, "~") + str(60)
high_score[4] = "name1: ".ljust(16, "~") + str(40)
high_score[5] = "name1: ".ljust(16, "~") + str(20)

def high_scores_table():
    high_scores_file = open("highscores.txt", "r")
    Print(3, "High Scores", Black, 100, 90)
    for s in high_score:
        Print(2, high_score[s], Black, 100, s*50+150)
    high_scores_file.close
    high_scores_file = open("highscores.txt", "a")
    for s in high_score:
        high_scores_file.write(high_score[s])
    high_scores_file.close()
# Set a high score table that can be saved and added to
    score[name] = score1
"""


# *****----*****----*****--- DRAW THE START MENU ---*****----*****----*****
def start_menu_draw():
    Print(4, "Welcome to", Red2, "center", 60)
    Print(5, "Bob the Jumper", Red2, "center", 165)
    Print(2, "A.K.A. Joel's Test Game", Black, "center", 270)
    start_true.draw(screen_x / 2 - 250, 350)
    player_numbers.draw(screen_x / 2 - 250, 480)
    p_number.draw(screen_x / 2 + 170, 485)

    PLAYERS_X = (p_number.width - pygame.font.Font.size(p_number.font, p_number.text)[0]) / 2 + screen_x / 2 + 170
    PLAYERS_Y = (p_number.height - pygame.font.Font.size(p_number.font, p_number.text)[1]) / 2 + 485
    Print(4, str(Players), Black, PLAYERS_X, PLAYERS_Y)
    P1_color.draw(screen_x / 2 - 200, 610)

    P1_C_Y = (P1_color.height - pygame.font.Font.size(P1_color.font, P1_color.text)[1]) / 2 + 610
    Print(4, P_Colors[P1_Select], Black, "center", P1_C_Y)
    P1_color_left.draw(screen_x / 2 - 300, 615)
    P1_color_right.draw(screen_x / 2 + 225, 615)
    P1_Image = pygame.image.load("Sprites/" + P_Images[P1_Select]).convert_alpha()
    screen.blit(P1_Image, (screen_x / 2 + 325, 610))
    if Players == 2:
        P2_color.draw(screen_x / 2 - 200, 740)
        P2_C_Y = (P2_color.height - pygame.font.Font.size(P2_color.font, P2_color.text)[1]) / 2 + 740
        Print(4, P_Colors[P2_Select], Black, "center", P2_C_Y)
        P2_color_left.draw(screen_x / 2 - 300, 745)
        P2_color_right.draw(screen_x / 2 + 225, 745)
        P2_Image = pygame.image.load("Sprites/" + P_Images[P2_Select]).convert_alpha()
        screen.blit(P2_Image, (screen_x / 2 + 325, 740))
        start_false.draw(screen_x / 2 - 250, 870)
    else:
        start_false.draw(screen_x / 2 - 250, 740)


# player_color.text(4, "" + str(P_Colors[P1_Select]), Black, "center", "center")
# player2_color.text(4, "" + str(P_Colors[P2_Select]), Black, "center", "center")


def instructions_draw():
    Print(2, "P1: Left", Black, 1350, 90)
    Print(2, "/   P2: A", Black, 1520, 90)
    Print(2, "= Move Left", Black, 1660, 90)
    Print(2, "P1: Right", Black, 1350, 130)
    Print(2, "/   P2: D", Black, 1520, 130)
    Print(2, "= Move Right", Black, 1660, 130)
    Print(2, "P1: Up", Black, 1350, 170)
    Print(2, "/   P2: W", Black, 1520, 170)
    Print(2, "= Jump", Black, 1660, 170)
    Print(2, "P1: Down", Black, 1350, 210)
    Print(2, "/   P2: S", Black, 1520, 210)
    Print(2, "= Stop Moving", Black, 1660, 210)
    Print(2, "Enter = Pause", Black, 1400, 260)
    Print(2, "Escape = Close Game", Black, 1400, 300)


# *****~~~~****~~~***~~**~ START THE MAIN PROGRAM ~**~~***~~~****~~~~*****
running = True
while running:
    all_sprites.update()
    screen.fill(White)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    clock.tick(FPS)

    # *****~~~~****~~~***~~**~ DEFINE THE GAME COMMANDS ~**~~***~~~****~~~~*****
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        # *****----*****----*****--- START MENU COMMANDS ---*****----*****----*****
        if start_menu_on:
            if event.type == MOUSEBUTTONDOWN:
                # *****----****----***----**--- CLICK THE START BUTTON ---**----***----****----*****
                if start_true.click:
                    player1 = Player("Sprites/" + P_Images[P1_Select])
                    player1.rect.x = 100
                    player2 = Player("Sprites/" + P_Images[P2_Select])
                    if Players == 2:
                        player2.rect.x = 50
                    else:
                        player2.kill()
                    start_menu_on = False
                    main_game_on = True
                    Ground_Generate()
                    main_music.play(loops=-1)
                # *****----****----***----**--- CHANGE PLAYER1 COLOR ---**----***----****----*****
                if P1_color_left.click:
                    # 0 to 5
                    if Players == 1:
                        if P1_Select > 0:
                            P1_Select -= 1
                        else:
                            P1_Select = P_Options
                    if Players == 2:
                        if P1_Select > 0 and P1_Select != P2_Select + 1:
                            P1_Select -= 1
                        elif P1_Select > 1 and P1_Select == P2_Select + 1:
                            P1_Select -= 2
                        elif P1_Select == 0 and P2_Select != P_Options:
                            P1_Select = P_Options
                        elif P1_Select == 1 and P2_Select == 0:
                            P1_Select = P_Options
                        elif P1_Select == 0 and P2_Select == P_Options:
                            P1_Select = P_Options - 1
                if P1_color_right.click:
                    if Players == 1:
                        if P1_Select < P_Options:
                            P1_Select += 1
                        else:
                            P1_Select = 0
                    if Players == 2:
                        if P1_Select < P_Options and P1_Select != P2_Select - 1:
                            P1_Select += 1
                        elif P1_Select < P_Options - 1 and P1_Select == P2_Select - 1:
                            P1_Select += 2
                        elif P1_Select == P_Options and P2_Select != 0:
                            P1_Select = 0
                        elif P1_Select == P_Options and P2_Select == 0:
                            P1_Select = 1
                        elif P1_Select == P_Options - 1 and P2_Select == P_Options:
                            P1_Select = 0
                # *****----****----***----**--- CHANGE PLAYER2 COLOR ---**----***----****----*****
                if Players == 2:
                    if P2_color_left.click:
                        if P2_Select > 0 and P2_Select != P1_Select + 1:
                            P2_Select -= 1
                        elif P2_Select > 1 and P2_Select == P1_Select + 1:
                            P2_Select -= 2
                        elif P2_Select == 0 and P1_Select != P_Options:
                            P2_Select = P_Options
                        elif P2_Select == 1 and P1_Select == 0:
                            P2_Select = P_Options
                        elif P2_Select == 0 and P1_Select == P_Options:
                            P2_Select = P_Options - 1
                    if P2_color_right.click:
                        if P2_Select < P_Options and P2_Select != P1_Select - 1:
                            P2_Select += 1
                        elif P2_Select < P_Options - 1 and P2_Select == P1_Select - 1:
                            P2_Select += 2
                        elif P2_Select == P_Options and P1_Select != 0:
                            P2_Select = 0
                        elif P2_Select == P_Options and P1_Select == 0:
                            P2_Select = 1
                        elif P2_Select == P_Options - 1 and P1_Select == P_Options:
                            P2_Select = 0
                # *****----****----***----**--- CHANGE NUMBER OF PLAYERS ---**----***----****----*****
                if p_number.click:
                    if Players == 1:
                        Players = 2
                    elif Players == 2:
                        Players = 1
                # *****----****----***----**--- CLICK THE QUIT BUTTON ---**----***----****----*****
                if start_false.click:
                    running = False

        # *****----*****----*****--- MAIN GAME COMMANDS ---*****----*****----*****
        if main_game_on:
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player1.movex = -walk
                    player1.face = "left"
                if event.key == K_RIGHT:
                    player1.movex = walk
                    player1.face = "right"
                if event.key == K_DOWN:
                    player1.movex = 0
                if event.key == K_UP and player1.grounded:
                    player1.movey -= jump
                    player1.grounded = False
                    sfx_jump.play()
                if event.key == K_a:
                    player2.movex = -walk
                    player2.face = "left"
                if event.key == K_d:
                    player2.movex = walk
                    player2.face = "right"
                if event.key == K_s:
                    player2.movex = 0
                if event.key == K_w and player2.grounded:
                    player2.movey -= jump
                    player2.grounded = False
                if event.key == K_RETURN:
                    Pause = True

    # RUNNING THE START MENU
    if start_menu_on:
        start_menu_draw()
        instructions_draw()
        # high_scores_table()
        Current_Time()
        # High Score field

    # RUNNING THE MAIN GAME
    if main_game_on:
        # MAIN GAMEPLAY COMMANDS
        backdrop_draw()
        Current_Time()

        # UPDATE PER TICK DURING GAMEPLAY
        # Increases exponentially at higher scores
        if Players == 1:
            if P1_Score > 5:
                Passing += 1
            if P1_Score > 15:
                Passing += 1
            if P1_Score > 25:
                Passing += 1
            if P1_Score > 35:
                Passing += 1
            if P1_Score > 45:
                Passing += 1
        if Players == 2:
            if P1_Score + P2_Score > 6:
                Passing += 1
            if P1_Score + P2_Score > 18:
                Passing += 1
            if P1_Score + P2_Score > 30:
                Passing += 1
            if P1_Score + P2_Score > 42:
                Passing += 1
            if P1_Score + P2_Score > 54:
                Passing += 1
        Passing += 1
        Make_Goober()
        all_players.update()
        all_goobers.update()
        all_sprites.draw(screen)
        if player1.lives <= 0:
            player_dead = True
            main_music.stop()
        if player2.lives <= 0:
            player_dead = True
            main_music.stop()

    # A PLAYER HAS DIED
    while player_dead:
        pygame.draw.rect(screen, Gray1, (int(screen_x / 6), int(screen_y / 3), int(screen_x / 1.5), 250))
        Print(4, "You struck too many Goobers", Red2, "center", 400)
        Print(2, "Press ESCAPE to go back to the main menu", Black, "center", 490)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    start_menu_on = True
                    main_game_on = False
                    player_dead = False
                    P1_Score = P2_Score = 0
                    for x in all_sprites:
                        x.kill()
        pygame.display.update()

    # PAUSE MENU
    while Pause:
        Print(4, "PAUSED", Gray3, "center", 400)
        instructions_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    Pause = False
                if event.key == K_RETURN:
                    Pause = False
        pygame.display.update()

    # Refresh the main display
    pygame.display.flip()
pygame.quit()
