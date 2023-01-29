import pygame as pg
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
pg.init()
main_music = pg.mixer.Sound("SFX/levelmusic.wav")
main_music.set_volume(0.55)
sfx_jump = pg.mixer.Sound("SFX/quickjump.wav")
sfx_jump.set_volume(0.9)
sfx_hit_head = pg.mixer.Sound("SFX/blockhit.wav")
sfx_hit_head.set_volume(0.85)
sfx_dead = pg.mixer.Sound("SFX/playerlosing.wav")
sfx_dead.set_volume(0.90)
sfx_goober_kill = pg.mixer.Sound("SFX/retrosquish.wav")
sfx_goober_kill.set_volume(0.9)
