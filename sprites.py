import random
import pygame as pg
import display as dp
from display import _print
import settings as stt


# *****----*****----*****--- DEFINE THE GAME DISPLAY ---*****----*****----*****
bd_sky = pg.image.load("Backdrops/Sky.png").convert()  # 500x600
bd_grass = pg.image.load("Backdrops/Grass.png").convert()  # 500x300


def backdrop_draw():
    dp.screen.fill(dp.Cyan1)
    for x in range(4):
        dp.screen.blit(bd_sky, (x * 500 - 25, 200))
        dp.screen.blit(bd_grass, (x * 500 - 25, 800))
    _print(4, "Jump on the", dp.Black, "center", 20)
    _print(4, "Goobers", dp.Black, "center", 110)
    _print(2, "Player1 Score: " + str(stt.P1_Score), dp.Black, 50, 45)
    _print(2, "Lives: ", dp.Black, 375, 45)
    if player1.lives >= 1:
        dp.screen.blit(player1.image_mini, (485, 40))
    if player1.lives >= 2:
        dp.screen.blit(player1.image_mini, (510, 40))
    if player1.lives >= 3:
        dp.screen.blit(player1.image_mini, (535, 40))
    if stt.Players == 2:
        _print(2, "Player2 Score: " + str(stt.P2_Score), dp.Black, 50, 105)
        _print(2, "Lives: ", dp.Black, 375, 105)
        if player2.lives >= 1:
            dp.screen.blit(player2.image_mini, (485, 100))
        if player2.lives >= 2:
            dp.screen.blit(player2.image_mini, (510, 100))
        if player2.lives >= 3:
            dp.screen.blit(player2.image_mini, (535, 100))


class Platform(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        if image == "clear":
            self.image = pg.Surface([dp.screen_x, dp.screen_y - 800])
            self.image.fill(dp.White)
            self.image.set_colorkey(dp.White)
        else:
            self.image = pg.image.load(image).convert()
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


# *****~~~~****~~~***~~**~ DEFINE THE GAME SPRITES ~**~~***~~~****~~~~*****
all_sprites = pg.sprite.Group()
all_ground = pg.sprite.Group()
all_players = pg.sprite.Group()
player1 = player2 = None


class Player(pg.sprite.Sprite):
    def __init__(self, image):
        self.move_x = 0
        self.move_y = 0
        self.lives = 3
        self.grounded = True
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image).convert_alpha()
        self.image_r = self.image
        self.image_l = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        mini_w = int(self.rect.width / 2)
        mini_h = int(self.rect.height / 2)
        self.image_mini = pg.transform.scale(self.image, (mini_w, mini_h))
        self.rect.bottom = 800
        all_sprites.add(self)
        all_players.add(self)

    def update(self):
        # ****---***---**--- ACTIVATE GRAVITY & MOVEMENT ---**---***---****
        self.move_y += stt.gravity
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.rect.left <= 20:
            self.rect.left = 25
        if self.rect.right >= dp.screen_x - 20:
            self.rect.right = dp.screen_x - 25
        if self.move_x > 0:
            self.image = self.image_r
        elif self.move_x < 0:
            self.image = self.image_l
        # ****---***---**--- COLLISION TEST AGAINST PLATFORMS ---**---***---****
        platform_hit = pg.sprite.spritecollide(self, all_ground, False)
        for g in platform_hit:
            # Hit your head on a platform
            if self.move_y < 0 and g.rect.left - 5 < self.rect.centerx < g.rect.right + 5:
                self.move_y = stt.gravity
                self.rect.top = g.rect.bottom
                stt.sfx_hit_head.play()
            # Landing atop a platform
            elif self.move_y > 0 and g.rect.left - 5 < self.rect.centerx < g.rect.right + 5:
                self.move_y = 0
                self.rect.bottom = g.rect.top
                self.grounded = True
            # Hit the left side of a platform
            elif self.rect.left < g.rect.left:
                if self.move_x > 0:
                    self.move_x = 0
                self.rect.right = g.rect.left - stt.walk
            # Hit the right side of a platform
            elif self.rect.right > g.rect.right:
                if self.move_x < 0:
                    self.move_x = 0
                self.rect.left = g.rect.right + stt.walk


# *****----*****----*****--- DEFINE THE GOOBERS ---*****----*****----*****
all_goobers = pg.sprite.Group()


class Goober(pg.sprite.Sprite):
    def __init__(self, image, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(dp.screen_x, 750))
        self.speed = speed
        self.move_y = 0
        if self.speed == 11:
            self.rect.y = 500
        self.Dead = False
        self.dead = int(dp.FPS * 1.25)
        all_sprites.add(self)
        all_goobers.add(self)
        stt.Passing = 0

    def update(self):
        self.move_y += stt.gravity
        self.rect.x -= self.speed
        self.rect.y += self.move_y
        if self.Dead:
            stt.sfx_goober_kill.play()
            self.dead -= 1
            if self.dead % 6 >= 3:
                self.image = pg.image.load("Sprites/GooberCrushed1.png").convert_alpha()
            if self.dead % 6 <= 2:
                self.image = pg.image.load("Sprites/GooberCrushed2.png").convert_alpha()
            self.rect.y += 25
            if self.dead > 0 and self.speed == 6:
                _print(2, "+1", dp.Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 8:
                _print(2, "+1", dp.Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 9:
                _print(2, "+2", dp.Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 10:
                _print(2, "+2", dp.Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 12:
                _print(2, "+3", dp.Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead > 0 and self.speed == 11:
                _print(2, "+3", dp.Red2, self.rect.x + 5, self.rect.y - 100)
            if self.dead == 0:
                pg.sprite.Sprite.kill(self)
        # ****---***---**--- CHECK FOR A PLAYER COLLISION ---**---***---****
        if pg.sprite.collide_rect(self, player1) and not self.Dead:
            if player1.move_y > 0 and not player1.grounded:
                if self.speed == 6:
                    stt.P1_Score += 1
                if self.speed == 8:
                    stt.P1_Score += 1
                if self.speed == 9:
                    stt.P1_Score += 2
                if self.speed == 10:
                    stt.P1_Score += 2
                if self.speed == 12:
                    stt.P1_Score += 3
                if self.speed == 11:
                    stt.P1_Score += 3
                self.Dead = True
                player1.rect.y -= 5
            else:
                player1.lives -= 1
                player1.rect.x = 75
                player1.rect.y = 225
                player1.move_x = 0
                stt.sfx_dead.play()
                if stt.Players == 1:
                    stt.Passing = 20
                    for x in all_goobers:
                        x.kill()
                    return
        if pg.sprite.collide_rect(self, player2) and not self.dead:
            if player2.movey > 0 and not player2.grounded:
                if self.speed == 6:
                    stt.P2_Score += 1
                if self.speed == 8:
                    stt.P2_Score += 1
                if self.speed == 9:
                    stt.P2_Score += 2
                if self.speed == 10:
                    stt.P2_Score += 2
                if self.speed == 12:
                    stt.P2_Score += 3
                if self.speed == 11:
                    stt.P2_Score += 3
                self.Dead = True
                player2.rect.y -= 5
            else:
                player2.lives -= 1
                player2.rect.x = 50
                player2.rect.y = 225
                player2.move_x = 0
                stt.sfx_dead.play()
        # ****---***---**--- CHECK FOR GROUND & PLATFORM ---**---***---****
        ground_land = pg.sprite.spritecollide(self, all_ground, False)
        for g in ground_land:
            # Hit its head on a platform
            if self.move_y < 0:
                self.move_y = stt.gravity
                self.rect.top = g.rect.bottom
            # Hit the side of a platform
            elif self.rect.left > g.rect.right - self.speed:
                self.move_y = stt.gravity
                self.rect.left = g.rect.right + 5
            # Landing atop a platform
            elif self.move_y > 0:
                self.move_y = 0
                self.rect.bottom = g.rect.top
                if self.speed == 9 and self.move_y >= 0 and random.randrange(0, 10) == 1:
                    self.move_y = -38
                if self.speed == 12 and self.move_y >= 0 and random.randrange(0, 8) == 1:
                    self.move_y = -45
        if self.speed == 11 and self.rect.y <= 400:
            self.move_y += 5
        if self.speed == 11 and self.rect.y >= 575:
            self.move_y -= 15
        if self.rect.right <= 0:
            pg.sprite.Sprite.kill(self)
            stt.Passing += 5


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
    if (stt.P1_Score + stt.P2_Score) <= 10:
        if stt.Passing >= 35 and spawn >= 80:
            Goober(G_Brown, 6)
    # Score under 15
    elif 10 < (stt.P1_Score + stt.P2_Score) <= 15:
        if stt.Passing >= 35 and spawn >= 85:
            Goober(G_Brown, 6)
        elif stt.Passing >= 40 and spawn >= 75:
            Goober(G_Green, 8)
    # Score under 20
    elif 15 < (stt.P1_Score + stt.P2_Score) <= 20:
        if stt.Passing >= 35 and spawn >= 86:
            Goober(G_Brown, 6)
        elif stt.Passing >= 40 and spawn >= 78:
            Goober(G_Green, 8)
        elif stt.Passing >= 45 and spawn >= 65:
            Goober(G_Blue, 9)
    # Score under 25
    elif 20 < (stt.P1_Score + stt.P2_Score) <= 25:
        if stt.Passing >= 32 and spawn >= 90:
            Goober(G_Brown, 6)
        elif stt.Passing >= 35 and spawn >= 80:
            Goober(G_Green, 8)
        elif stt.Passing >= 40 and spawn >= 72:
            Goober(G_Blue, 9)
        elif stt.Passing >= 45 and spawn >= 60:
            Goober(G_Red, 10)
    # Score under 30
    elif 25 < (stt.P1_Score + stt.P2_Score) <= 30:
        if stt.Passing >= 32 and spawn >= 92:
            Goober(G_Brown, 6)
        elif stt.Passing >= 36 and spawn >= 84:
            Goober(G_Green, 8)
        elif stt.Passing >= 40 and spawn >= 78:
            Goober(G_Blue, 9)
        elif stt.Passing >= 44 and spawn >= 70:
            Goober(G_Red, 10)
        elif stt.Passing >= 48 and spawn >= 60:
            Goober(G_Black, 12)
    # Score under 35
    elif 30 < (stt.P1_Score + stt.P2_Score) <= 35:
        if stt.Passing >= 32 and spawn >= 92:
            Goober(G_Brown, 6)
        elif stt.Passing >= 34 and spawn >= 84:
            Goober(G_Green, 8)
        elif stt.Passing >= 36 and spawn >= 78:
            Goober(G_Blue, 9)
        elif stt.Passing >= 38 and spawn >= 70:
            Goober(G_Red, 10)
        elif stt.Passing >= 40 and spawn >= 60:
            Goober(G_Black, 12)
    # Score under 40
    elif 35 < (stt.P1_Score + stt.P2_Score) <= 40:
        if stt.Passing >= 30 and spawn >= 95:
            Goober(G_Brown, 6)
        elif stt.Passing >= 33 and spawn >= 88:
            Goober(G_Green, 8)
        elif stt.Passing >= 36 and spawn >= 82:
            Goober(G_Blue, 9)
        elif stt.Passing >= 39 and spawn >= 75:
            Goober(G_Red, 10)
        elif stt.Passing >= 42 and spawn >= 65:
            Goober(G_Black, 12)
        elif stt.Passing >= 46 and spawn >= 60:
            Goober(G_White, 11)
    # Score over 40
    elif (stt.P1_Score + stt.P2_Score) > 40:
        if stt.Passing >= 28 and spawn >= 96:
            Goober(G_Brown, 6)
        elif stt.Passing >= 30 and spawn >= 92:
            Goober(G_Green, 8)
        elif stt.Passing >= 32 and spawn >= 88:
            Goober(G_Blue, 9)
        elif stt.Passing >= 34 and spawn >= 80:
            Goober(G_Red, 10)
        elif stt.Passing >= 37 and spawn >= 72:
            Goober(G_Black, 12)
        elif stt.Passing >= 40 and spawn >= 64:
            Goober(G_White, 11)
