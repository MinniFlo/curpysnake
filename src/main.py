from GameSetup import Setup
import os
import curses
import argparse
from functools import partial


def main(args, scr):
    gamesetup = Setup(scr)
    gamesetup.game.game_loop()
    os.system("reset")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("test")
    args = parser.parse_args()

    curses.wrapper(partial(main, args))

