from GameSetup import Setup
import os
import curses
import argparse
from functools import partial


def main(args, scr):
    gamesetup = Setup(scr, args)
    game = gamesetup.create_game()
    game.game_loop()
    os.system("reset")


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()

    parser = argparse.ArgumentParser(prog='tool',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    parser.add_argument("-w", "--walls", help="deactivates movement through walls", action="store_true")
    parser.add_argument("-u", "--uglycolor", help="makes color ugly", action="store_true")
    parser.add_argument("-r", "--randomspeed", help="makes speed random", action="store_true")
    parser.add_argument("-c", "--color", type=int, help="choose snake color", choices=range(1, 4))
    args = parser.parse_args()

    curses.wrapper(partial(main, args))

