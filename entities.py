import arcade
import random
from settings import *

class Enemy(arcade.Sprite):
    def __init__(self, secs):
        super().__init__("pic/enemy.png", 0.1)
        self.center_x = random.randrange(20, W - 20)
        self.center_y = H + 20
        self.change_y = -(E_SPD + (secs / 100))
        self.hp = 1 + (secs // 15)
        self.max_hp = self.hp

    def draw_hp(self):
        w = self.width * (self.hp / self.max_hp)
        if w > 0:
            arcade.draw_rectangle_filled(self.center_x, self.top + 5, w, 4, arcade.color.GREEN)

class EnhancedEnemy(Enemy):
    def __init__(self, secs):
        super().__init__(secs)
        self.texture = arcade.load_texture("pic/enemy_enh.png")
        self.hp *= 2
        self.max_hp = self.hp

class SmallCube(arcade.Sprite):
    def __init__(self, x, y, secs):
        super().__init__("pic/minion.png", 0.1)
        self.center_x = x
        self.center_y = y
        self.change_y = -E_SPD * 1.5
        self.hp = max(1, secs // 30)
        self.max_hp = self.hp

    def draw_hp(self):
        w = self.width * (self.hp / self.max_hp)
        if w > 0:
            arcade.draw_rectangle_filled(self.center_x, self.top + 3, w, 2, arcade.color.GREEN)

class MiniBoss(arcade.Sprite):
    def __init__(self, secs):
        super().__init__("pic/miniboss.png", 0.2)
        self.center_x = random.randrange(30, W - 30)
        self.center_y = H + 30
        self.change_y = -E_SPD * 0.7
        self.hp = 30 + secs
        self.max_hp = self.hp

    def draw_hp(self):
        w = self.width * (self.hp / self.max_hp)
        if w > 0:
            arcade.draw_rectangle_filled(self.center_x, self.top + 5, w, 6, arcade.color.GREEN)

class Boss(arcade.Sprite):
    def __init__(self, secs, player_dmg):
        super().__init__("pic/boss.png", 0.3)
        self.center_x = W // 2
        self.center_y = H + 60
        self.base_speed = E_SPD * 0.4
        self.change_y = -self.base_speed
        self.hp = (100 * player_dmg) + (secs * 3)
        self.max_hp = self.hp
        self.is_boss = True
        self.state = 'spawning'
        self.timer = 0
        self.invulnerable = True
        self.alpha = 150

    def draw_hp(self):
        w = self.width * (self.hp / self.max_hp)
        if w > 0:
            c = arcade.color.GRAY if self.invulnerable else arcade.color.GREEN
            arcade.draw_rectangle_filled(self.center_x, self.top + 5, w, 8, c)

    def update_boss(self, e_list, secs):
        self.timer += 1
        if self.state == 'spawning':
            if self.timer >= 600:
                self.state = 'moving'
                self.timer = 0
                self.invulnerable = False
                self.alpha = 255
        elif self.state == 'moving':
            if self.timer >= 420:
                self.state = 'stopped'
                self.timer = 0
                self.change_y = 0
                self.invulnerable = True
                self.alpha = 150
        elif self.state == 'stopped':
            if self.timer % 60 == 0 and self.timer <= 600:
                for i in range(5):
                    spacing = W // 6
                    sc = SmallCube(spacing * (i + 1), self.bottom - 20, secs)
                    e_list.append(sc)
            if self.timer >= 600:
                self.state = 'moving'
                self.timer = 0
                self.change_y = -self.base_speed
                self.invulnerable = False
                self.alpha = 255


class PowerUp(arcade.Sprite):
    def __init__(self, t):
        files = {
            1: "pic/pu_dmg.png",
            2: "pic/pu_spd.png",
            3: "pic/pu_laser_b.png",
            4: "pic/pu_laser_m.png",
            5: "pic/pu_multi.png"
        }

        scales = {
            1: 0.05,
            2: 0.13,
            3: 0.2,
            4: 0.12,
            5: 0.05
        }

        super().__init__(files[t], scales[t])

        self.type_pu = t
        self.center_x = random.randrange(20, W - 20)
        self.center_y = H + 20
        self.change_y = -E_SPD

class Bullet(arcade.Sprite):
    def __init__(self, x, y, filename, d, n=False, scale= 0.1):
        super().__init__(filename, scale)
        self.center_x = x
        self.bottom = y
        self.change_y = B_SPD
        self.dmg = d
        self.is_nuke = n
        self.hit_list = set()