from GameWindow import Window
import os
import curses


def main(scr):
    game = Window(scr)
    game.game_loop()
    os.system("reset")


if __name__ == '__main__':
    curses.wrapper(main)

