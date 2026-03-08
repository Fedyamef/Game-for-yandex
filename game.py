import arcade
import random
from settings import *
from entities import Enemy, EnhancedEnemy, MiniBoss, Boss, PowerUp, Bullet


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.p_list = arcade.SpriteList()
        self.e_list = arcade.SpriteList()
        self.b_list = arcade.SpriteList()
        self.pu_list = arcade.SpriteList()
        self.p = arcade.Sprite("pic/player.png", 0.1)
        self.l_pr = False
        self.r_pr = False
        self.sc = 0
        self.over = False
        self.fr = 0
        self.dmg = 1
        self.shoot_timer = 0
        self.fire_rate = 20
        self.nuke_delay = 0
        self.nuke_type = 0
        self.attack_cooldown = 0
        self.multi = 1
        self.enh_timer = 0
        self.next_enh = random.randrange(360, 601)
        self.mini_timer = 0
        self.next_mini = random.randrange(600, 1201)
        self.boss_timer = 0
        self.next_boss = random.randrange(3000, 4201)
        self.boss_incoming = False
        self.boss_in_timer = 0
        self.boss_active = False

    def setup(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.bg = arcade.load_texture("pic/bg.png")
        self.p_list.clear()
        self.e_list.clear()
        self.b_list.clear()
        self.pu_list.clear()
        self.p.center_x = W // 2
        self.p.center_y = 50
        self.p_list.append(self.p)
        self.sc = 0
        self.over = False
        self.fr = 0
        self.dmg = 1
        self.shoot_timer = 0
        self.fire_rate = 20
        self.nuke_delay = 0
        self.nuke_type = 0
        self.attack_cooldown = 0
        self.multi = 1
        self.enh_timer = 0
        self.next_enh = random.randrange(360, 601)
        self.mini_timer = 0
        self.next_mini = random.randrange(600, 1201)
        self.boss_timer = 0
        self.next_boss = random.randrange(3000, 4201)
        self.boss_incoming = False
        self.boss_in_timer = 0
        self.boss_active = False

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, W, H, self.bg)
        self.p_list.draw()
        self.e_list.draw()
        self.b_list.draw()
        self.pu_list.draw()

        for e in self.e_list:
            e.draw_hp()

        arcade.draw_text(f"Счет: {self.sc}  Урон: {self.dmg}", 10, H - 30, arcade.color.WHITE, 16)

        if self.boss_incoming:
            arcade.draw_text("WARNING: BOSS INCOMING", W // 2, H // 2 + 100, arcade.color.RED, 25, anchor_x="center")

        if self.over:
            arcade.draw_text("GAME OVER", W // 2, H // 2 + 50, arcade.color.RED, 40, anchor_x="center")
            arcade.draw_rectangle_filled(W // 2, H // 2 - 20, 200, 50, arcade.color.DARK_GRAY)
            arcade.draw_text("В меню", W // 2, H // 2 - 30, arcade.color.WHITE, 20, anchor_x="center")

    def on_mouse_press(self, x, y, b, mods):
        if self.over and W // 2 - 100 < x < W // 2 + 100 and H // 2 - 45 < y < H // 2 + 5:
            import menu
            self.window.show_view(menu.MainMenu())

    def on_update(self, dt):
        if self.over: return

        self.p.change_x = 0
        if self.l_pr and not self.r_pr:
            self.p.change_x = -SPD
        elif self.r_pr and not self.l_pr:
            self.p.change_x = SPD

        self.p_list.update()
        self.b_list.update()
        self.e_list.update()
        self.pu_list.update()

        if self.p.left < 0:
            self.p.left = 0
        elif self.p.right > W:
            self.p.right = W

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.nuke_delay > 0:
            self.nuke_delay -= 1
            if self.nuke_delay == 0:
                if self.nuke_type == 1:
                    b = Bullet(self.p.center_x, self.p.top, "pic/laser_b.png", 30, True, 0.6)
                    self.attack_cooldown = 60
                else:
                    b = Bullet(self.p.center_x, self.p.top, "pic/laser_m.png", 10, True, 0.4)
                    self.attack_cooldown = 30
                self.b_list.append(b)

        elif self.attack_cooldown == 0 and self.nuke_delay == 0:
            self.shoot_timer += 1
            if self.shoot_timer >= self.fire_rate:
                self.shoot_timer = 0
                for i in range(self.multi):
                    offset = (i - (self.multi - 1) / 2) * 15
                    b = Bullet(self.p.center_x + offset, self.p.top, "pic/bullet.png", self.dmg)
                    self.b_list.append(b)

        self.fr += 1
        secs = self.fr // 60

        if not self.boss_incoming and not self.boss_active:
            self.boss_timer += 1
            if self.boss_timer >= self.next_boss:
                self.boss_incoming = True
                self.boss_in_timer = 0

        if self.boss_incoming:
            self.boss_in_timer += 1
            if self.boss_in_timer >= 300:
                self.boss_incoming = False
                self.boss_active = True
                self.e_list.append(Boss(secs, self.dmg))

        if self.boss_active:
            boss_alive = any(getattr(e, 'is_boss', False) for e in self.e_list)
            if not boss_alive:
                self.boss_active = False
                self.boss_timer = 0
                self.next_boss = random.randrange(3000, 4201)
                self.enh_timer = 0
                self.mini_timer = 0

        if not self.boss_incoming and not self.boss_active and self.fr > 180:
            cur_spawn = max(20, 90 - secs)
            if self.fr % cur_spawn == 0:
                self.e_list.append(Enemy(secs))

            self.enh_timer += 1
            if self.enh_timer >= self.next_enh:
                self.enh_timer = 0
                self.next_enh = random.randrange(360, 601)
                self.e_list.append(EnhancedEnemy(secs))

            self.mini_timer += 1
            if self.mini_timer >= self.next_mini:
                self.mini_timer = 0
                self.next_mini = random.randrange(600, 1201)
                self.e_list.append(MiniBoss(secs))

        can_spawn_pu = False
        if len(self.pu_list) < 3:
            if len(self.pu_list) == 0:
                can_spawn_pu = True
            else:
                last_pu = self.pu_list[-1]
                if last_pu.center_y <= (H + 20) - (H / 3):
                    can_spawn_pu = True

        if can_spawn_pu and random.randrange(60) == 0:
            t = random.choices([1, 2, 3, 4, 5], weights=[40, 15, 5, 20, 10])[0]
            self.pu_list.append(PowerUp(t))

        for b in self.b_list:
            if b.bottom > H:
                b.remove_from_sprite_lists()
            else:
                hits = arcade.check_for_collision_with_list(b, self.e_list)
                if hits:
                    if not b.is_nuke:
                        b.remove_from_sprite_lists()

                    for e in hits:
                        if getattr(e, 'invulnerable', False):
                            continue

                        if getattr(b, 'is_nuke', False):
                            if e in b.hit_list:
                                continue
                            b.hit_list.add(e)

                        e.hp -= b.dmg
                        if e.hp <= 0:
                            if e in self.e_list:
                                e.remove_from_sprite_lists()
                                self.sc += 1

        for e in self.e_list:
            if getattr(e, 'is_boss', False):
                e.update_boss(self.e_list, secs)
            if e.bottom < 0:
                self.over = True

        for pu in self.pu_list:
            if pu.bottom < 0:
                pu.remove_from_sprite_lists()
            elif arcade.check_for_collision(pu, self.p):
                t = pu.type_pu
                pu.remove_from_sprite_lists()

                if t == 1:
                    self.dmg += 1
                elif t == 2:
                    self.fire_rate = max(5, self.fire_rate - 2)
                elif t == 3:
                    self.nuke_delay = 90
                    self.nuke_type = 1
                elif t == 4:
                    self.nuke_delay = 30
                    self.nuke_type = 2
                elif t == 5:
                    self.multi = min(5, self.multi + 1)

        if arcade.check_for_collision_with_list(self.p, self.e_list):
            self.over = True

    def on_key_press(self, key, mods):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.l_pr = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.r_pr = True

    def on_key_release(self, key, mods):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.l_pr = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.r_pr = False