import arcade
from menu import MainMenu
from settings import W, H

if __name__ == "__main__":
    w = arcade.Window(W, H, "Arcade Game")
    v = MainMenu()
    w.show_view(v)
    arcade.run()