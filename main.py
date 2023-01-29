# Program: Jumper
#   A simple interactive game showing movement control, basic animations, and collisions
# Requires: pygame library
# Created by: Joel Leckie
# May 2021 - Initial file creation
# July 2021 - v. 1 complete
# January 2023 - Additional refinements
#       - Split code into separate modules for display.py, settings.py, sprites.py, and main.py
#       - As of Jan. 28, 2023 separated modules not fully tested

import pygame as pg
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_a, K_s, K_d, K_w,
    K_RETURN, K_ESCAPE,
    KEYDOWN, MOUSEBUTTONDOWN)
import display as dp
from display import _print
import settings as stt
import sprites as spr

# *****~~~~****~~~***~~**~ START MENU DISPLAY ~**~~***~~~****~~~~*****


# ***---***---***-- DEFINE THE START MENU --***---***---***
start_true = dp.Button()
player_numbers = dp.Button()
p_number = dp.Button()
start_false = dp.Button()
P1_color = dp.Button()
P1_color_left = dp.Button()
P1_color_right = dp.Button()
P2_color = dp.Button()
P2_color_left = dp.Button()
P2_color_right = dp.Button()

start_true.text(4, "Start Game", dp.Black, "center", "center")
player_numbers.text(4, "Players: ", dp.Black, "center", "center")
p_number.text(4, "  ", dp.Black, "center", "center")
start_false.text(4, "Quit Game", dp.Black, "center", "center")
P1_color.text(4, " ", dp.Black, "center", "center")
P1_color_left.text(4, "<-", dp.Black, "center", "center")
P1_color_right.text(4, "->", dp.Black, "center", "center")
P2_color.text(4, " ", dp.Black, "center", "center")
P2_color_left.text(4, "<-", dp.Black, "center", "center")
P2_color_right.text(4, "->", dp.Black, "center", "center")

start_true.box(dp.Blue1, dp.Green1, 500, 95, 5, dp.Black)
player_numbers.box(dp.Blue1, "same", 400, 95, 5, dp.Black)
p_number.box(dp.Cyan2, dp.Green1, 80, 85, 5, dp.Purple2)
start_false.box(dp.Blue1, dp.Green1, 500, 95, 5, dp.Black)
P1_color.box(dp.Blue1, "same", 400, 95, 5, dp.Black)
P1_color_left.box(dp.Blue1, dp.Green1, 75, 85, 5, dp.Black)
P1_color_right.box(dp.Blue1, dp.Green1, 75, 85, 5, dp.Black)
P2_color.box(dp.Blue1, "same", 400, 95, 5, dp.Black)
P2_color_left.box(dp.Blue1, dp.Green1, 75, 85, 5, dp.Black)
P2_color_right.box(dp.Blue1, dp.Green1, 75, 85, 5, dp.Black)

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
    _print(3, "High Scores", Black, 100, 90)
    for s in high_score:
        _print(2, high_score[s], Black, 100, s*50+150)
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
    _print(4, "Welcome to", dp.Red2, "center", 60)
    _print(5, "Bob the Jumper", dp.Red2, "center", 165)
    _print(2, "A.K.A. Joel's Test Game", dp.Black, "center", 270)
    start_true.draw(dp.screen_x / 2 - 250, 350)
    player_numbers.draw(dp.screen_x / 2 - 250, 480)
    p_number.draw(dp.screen_x / 2 + 170, 485)

    PLAYERS_X = (p_number.width - pg.font.Font.size(p_number.font, p_number.text)[0]) / 2 + dp.screen_x / 2 + 170
    PLAYERS_Y = (p_number.height - pg.font.Font.size(p_number.font, p_number.text)[1]) / 2 + 485
    _print(4, str(stt.Players), dp.Black, PLAYERS_X, PLAYERS_Y)
    P1_color.draw(dp.screen_x / 2 - 200, 610)

    P1_C_Y = (P1_color.height - pg.font.Font.size(P1_color.font, P1_color.text)[1]) / 2 + 610
    _print(4, stt.P_Colors[stt.P1_Select], dp.Black, "center", P1_C_Y)
    P1_color_left.draw(dp.screen_x / 2 - 300, 615)
    P1_color_right.draw(dp.screen_x / 2 + 225, 615)
    P1_Image = pg.image.load("Sprites/" + stt.P_Images[stt.P1_Select]).convert_alpha()
    dp.screen.blit(P1_Image, (dp.screen_x / 2 + 325, 610))
    if stt.Players == 2:
        P2_color.draw(dp.screen_x / 2 - 200, 740)
        P2_C_Y = (P2_color.height - pg.font.Font.size(P2_color.font, P2_color.text)[1]) / 2 + 740
        _print(4, stt.P_Colors[stt.P2_Select], dp.Black, "center", P2_C_Y)
        P2_color_left.draw(dp.screen_x / 2 - 300, 745)
        P2_color_right.draw(dp.screen_x / 2 + 225, 745)
        P2_Image = pg.image.load("Sprites/" + stt.P_Images[stt.P2_Select]).convert_alpha()
        dp.screen.blit(P2_Image, (dp.screen_x / 2 + 325, 740))
        start_false.draw(dp.screen_x / 2 - 250, 870)
    else:
        start_false.draw(dp.screen_x / 2 - 250, 740)


# player_color.text(4, "" + str(P_Colors[P1_Select]), Black, "center", "center")
# player2_color.text(4, "" + str(P_Colors[P2_Select]), Black, "center", "center")


def instructions_draw():
    _print(2, "P1: Left", dp.Black, 1350, 90)
    _print(2, "/   P2: A", dp.Black, 1520, 90)
    _print(2, "= Move Left", dp.Black, 1660, 90)
    _print(2, "P1: Right", dp.Black, 1350, 130)
    _print(2, "/   P2: D", dp.Black, 1520, 130)
    _print(2, "= Move Right", dp.Black, 1660, 130)
    _print(2, "P1: Up", dp.Black, 1350, 170)
    _print(2, "/   P2: W", dp.Black, 1520, 170)
    _print(2, "= Jump", dp.Black, 1660, 170)
    _print(2, "P1: Down", dp.Black, 1350, 210)
    _print(2, "/   P2: S", dp.Black, 1520, 210)
    _print(2, "= Stop Moving", dp.Black, 1660, 210)
    _print(2, "Enter = Pause", dp.Black, 1400, 260)
    _print(2, "Escape = Close Game", dp.Black, 1400, 300)


# *****~~~~****~~~***~~**~ START THE MAIN PROGRAM ~**~~***~~~****~~~~*****
running = True
while running:
    spr.all_sprites.update()
    dp.screen.fill(dp.White)
    dp.mouse_x, dp.mouse_y = pg.mouse.get_pos()
    mouse_click = pg.mouse.get_pressed()[0]
    pg.mouse.set_cursor(*pg.cursors.diamond)
    dp.clock.tick(dp.FPS)

    # *****~~~~****~~~***~~**~ DEFINE THE GAME COMMANDS ~**~~***~~~****~~~~*****
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        # *****----*****----*****--- START MENU COMMANDS ---*****----*****----*****
        if stt.start_menu_on:
            if event.type == MOUSEBUTTONDOWN:
                # *****----****----***----**--- CLICK THE START BUTTON ---**----***----****----*****
                if start_true.click:
                    spr.player1 = spr.Player("Sprites/" + stt.P_Images[stt.P1_Select])
                    spr.player1.rect.x = 100
                    spr.player2 = spr.Player("Sprites/" + stt.P_Images[stt.P2_Select])
                    if stt.Players == 2:
                        spr.player2.rect.x = 50
                    else:
                        spr.player2.kill()
                    start_menu_on = False
                    main_game_on = True
                    spr.Ground_Generate()
                    stt.main_music.play(loops=-1)
                # *****----****----***----**--- CHANGE PLAYER1 COLOR ---**----***----****----*****
                if P1_color_left.click:
                    # 0 to 5
                    if stt.Players == 1:
                        if stt.P1_Select > 0:
                            stt.P1_Select -= 1
                        else:
                            stt.P1_Select = stt.P_Options
                    if stt.Players == 2:
                        if stt.P1_Select > 0 and stt.P1_Select != stt.P2_Select + 1:
                            stt.P1_Select -= 1
                        elif stt.P1_Select > 1 and stt.P1_Select == stt.P2_Select + 1:
                            stt.P1_Select -= 2
                        elif stt.P1_Select == 0 and stt.P2_Select != stt.P_Options:
                            stt.P1_Select = stt.P_Options
                        elif stt.P1_Select == 1 and stt.P2_Select == 0:
                            stt.P1_Select = stt.P_Options
                        elif stt.P1_Select == 0 and stt.P2_Select == stt.P_Options:
                            stt.P1_Select = stt.P_Options - 1
                if P1_color_right.click:
                    if stt.Players == 1:
                        if stt.P1_Select < stt.P_Options:
                            stt.P1_Select += 1
                        else:
                            stt.P1_Select = 0
                    if stt.Players == 2:
                        if stt.P1_Select < stt.P_Options and stt.P1_Select != stt.P2_Select - 1:
                            stt.P1_Select += 1
                        elif stt.P1_Select < stt.P_Options - 1 and stt.P1_Select == stt.P2_Select - 1:
                            stt.P1_Select += 2
                        elif stt.P1_Select == stt.P_Options and stt.P2_Select != 0:
                            stt.P1_Select = 0
                        elif stt.P1_Select == stt.P_Options and stt.P2_Select == 0:
                            stt.P1_Select = 1
                        elif stt.P1_Select == stt.P_Options - 1 and stt.P2_Select == stt.P_Options:
                            stt.P1_Select = 0
                # *****----****----***----**--- CHANGE PLAYER2 COLOR ---**----***----****----*****
                if stt.Players == 2:
                    if P2_color_left.click:
                        if stt.P2_Select > 0 and stt.P2_Select != stt.P1_Select + 1:
                            stt.P2_Select -= 1
                        elif stt.P2_Select > 1 and stt.P2_Select == stt.P1_Select + 1:
                            stt.P2_Select -= 2
                        elif stt.P2_Select == 0 and stt.P1_Select != stt.P_Options:
                            stt.P2_Select = stt.P_Options
                        elif stt.P2_Select == 1 and stt.P1_Select == 0:
                            stt.P2_Select = stt.P_Options
                        elif stt.P2_Select == 0 and stt.P1_Select == stt.P_Options:
                            stt.P2_Select = stt.P_Options - 1
                    if P2_color_right.click:
                        if stt.P2_Select < stt.P_Options and stt.P2_Select != stt.P1_Select - 1:
                            stt.P2_Select += 1
                        elif stt.P2_Select < stt.P_Options - 1 and stt.P2_Select == stt.P1_Select - 1:
                            stt.P2_Select += 2
                        elif stt.P2_Select == stt.P_Options and stt.P1_Select != 0:
                            stt.P2_Select = 0
                        elif stt.P2_Select == stt.P_Options and stt.P1_Select == 0:
                            stt.P2_Select = 1
                        elif stt.P2_Select == stt.P_Options - 1 and stt.P1_Select == stt.P_Options:
                            stt.P2_Select = 0
                # *****----****----***----**--- CHANGE NUMBER OF PLAYERS ---**----***----****----*****
                if p_number.click:
                    if stt.Players == 1:
                        stt.Players = 2
                    elif stt.Players == 2:
                        stt.Players = 1
                # *****----****----***----**--- CLICK THE QUIT BUTTON ---**----***----****----*****
                if start_false.click:
                    running = False

        # *****----*****----*****--- MAIN GAME COMMANDS ---*****----*****----*****
        if stt.main_game_on:
            if event.type == pg.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    spr.player1.move_x = -stt.walk
                    spr.player1.face = "left"
                if event.key == K_RIGHT:
                    spr.player1.move_x = stt.walk
                    spr.player1.face = "right"
                if event.key == K_DOWN:
                    spr.player1.move_x = 0
                if event.key == K_UP and spr.player1.grounded:
                    spr.player1.move_y -= stt.jump
                    spr.player1.grounded = False
                    stt.sfx_jump.play()
                if event.key == K_a:
                    spr.player2.move_x = -stt.walk
                    spr.player2.face = "left"
                if event.key == K_d:
                    spr.player2.move_x = stt.walk
                    spr.player2.face = "right"
                if event.key == K_s:
                    spr.player2.move_x = 0
                if event.key == K_w and spr.player2.grounded:
                    spr.player2.move_y -= stt.jump
                    spr.player2.grounded = False
                if event.key == K_RETURN:
                    Pause = True

    # RUNNING THE START MENU
    if stt.start_menu_on:
        start_menu_draw()
        instructions_draw()
        # high_scores_table()
        dp.CurrentTime()
        # High Score field

    # RUNNING THE MAIN GAME
    if stt.main_game_on:
        # MAIN GAMEPLAY COMMANDS
        spr.backdrop_draw()
        dp.CurrentTime()

        # UPDATE PER TICK DURING GAMEPLAY
        # Increases exponentially at higher scores
        if stt.Players == 1:
            if stt.P1_Score > 5:
                stt.Passing += 1
            if stt.P1_Score > 15:
                stt.Passing += 1
            if stt.P1_Score > 25:
                stt.Passing += 1
            if stt.P1_Score > 35:
                stt.Passing += 1
            if stt.P1_Score > 45:
                stt.Passing += 1
        if stt.Players == 2:
            if stt.P1_Score + stt.P2_Score > 6:
                stt.Passing += 1
            if stt.P1_Score + stt.P2_Score > 18:
                stt.Passing += 1
            if stt.P1_Score + stt.P2_Score > 30:
                stt.Passing += 1
            if stt.P1_Score + stt.P2_Score > 42:
                stt.Passing += 1
            if stt.P1_Score + stt.P2_Score > 54:
                stt.Passing += 1
        stt.Passing += 1
        spr.Make_Goober()
        spr.all_players.update()
        spr.all_goobers.update()
        spr.all_sprites.draw(dp.screen)
        if spr.player1.lives <= 0:
            player_dead = True
            stt.main_music.stop()
        if spr.player2.lives <= 0:
            player_dead = True
            stt.main_music.stop()

    # A PLAYER HAS DIED
    while stt.player_dead:
        pg.draw.rect(dp.screen, dp.Gray1, (int(dp.screen_x / 6), int(dp.screen_y / 3), int(dp.screen_x / 1.5), 250))
        _print(4, "You struck too many Goobers", dp.Red2, "center", 400)
        _print(2, "Press ESCAPE to go back to the main menu", dp.Black, "center", 490)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    start_menu_on = True
                    main_game_on = False
                    player_dead = False
                    P1_Score = P2_Score = 0
                    for x in spr.all_sprites:
                        x.kill()
        pg.display.update()

    # PAUSE MENU
    while stt.Pause:
        _print(4, "PAUSED", dp.Gray3, "center", 400)
        instructions_draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                stt.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stt.running = False
                    stt.Pause = False
                if event.key == K_RETURN:
                    stt.Pause = False
        pg.display.update()

    # Refresh the main display
    pg.display.flip()
pg.quit()
