import arcade
from settings import W, H


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg = arcade.load_texture("pic/bgm.jpg")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, W, H, self.bg)
        arcade.draw_text("KNIGHT VS BOBRS", W // 2, H - 150, arcade.color.WHITE, 35, anchor_x="center")

        arcade.draw_rectangle_filled(W // 2, H // 2 + 50, 200, 50, arcade.color.DARK_GREEN)
        arcade.draw_text("Старт", W // 2, H // 2 + 40, arcade.color.WHITE, 20, anchor_x="center")

        arcade.draw_rectangle_filled(W // 2, H // 2 - 20, 200, 50, arcade.color.DARK_BLUE)
        arcade.draw_text("Инструкция", W // 2, H // 2 - 30, arcade.color.WHITE, 20, anchor_x="center")

        arcade.draw_rectangle_filled(W // 2, H // 2 - 90, 200, 50, arcade.color.DARK_RED)
        arcade.draw_text("Выход", W // 2, H // 2 - 100, arcade.color.WHITE, 20, anchor_x="center")

    def on_mouse_press(self, x, y, b, mods):
        if W // 2 - 100 < x < W // 2 + 100:
            if H // 2 + 25 < y < H // 2 + 75:
                from game import Game
                g = Game()
                g.setup()
                self.window.show_view(g)
            elif H // 2 - 45 < y < H // 2 + 5:
                self.window.show_view(Instructions())
            elif H // 2 - 115 < y < H // 2 - 65:
                arcade.exit()


class Instructions(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg = arcade.load_texture("pic/bgm.jpg")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, W, H, self.bg)
        arcade.draw_rectangle_filled(W // 2, H // 2, W, H, (0, 0, 0, 180))
        arcade.draw_text("ИНСТРУКЦИЯ", W // 2, H - 100, arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("Стрельба: Автоматическая", W // 2, H - 200, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Движение: СТРЕЛКИ / A D", W // 2, H - 250, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Все, что не похоже на бобров - бафы", W // 2, H - 300, arcade.color.GREEN, 20,
                         anchor_x="center")
        arcade.draw_text("Бобры - враги", W // 2, H - 350, arcade.color.RED, 20,
                         anchor_x="center")

        arcade.draw_rectangle_filled(W // 2, 100, 200, 50, arcade.color.DARK_GRAY)
        arcade.draw_text("Назад", W // 2, 90, arcade.color.WHITE, 20, anchor_x="center")

    def on_mouse_press(self, x, y, b, mods):
        if W // 2 - 100 < x < W // 2 + 100 and 75 < y < 125:
            self.window.show_view(MainMenu())