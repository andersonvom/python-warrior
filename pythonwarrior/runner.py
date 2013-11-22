import argparse
import sys

from pythonwarrior.config import Config
from pythonwarrior.game import Game


class Runner(object):
    def __init__(self, arguments, stdin=None, stdout=None):
        self.arguments = arguments[1:]  # skip program name
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.game = Game()

    def run(self):
        Config.in_stream = self.stdin
        Config.out_stream = self.stdout
        Config.delay = 0.6
        self.parse_options()
        self.game.start()

    def parse_options(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-d', '--directory', metavar='DIR',
                            help='Run under a given directory')
        parser.add_argument('-l', '--level', type=int,
                            help='Practice level on epic')
        parser.add_argument('-s', '--skip', action='store_true',
                            help='Skip user input')
        parser.add_argument('-t', '--time', metavar='SECONDS', type=float,
                            help='Delay each turn by seconds')
        args = parser.parse_args(self.arguments)

        if args.directory:
            Config.path_prefix = args.directory
        if args.level:
            Config.practice_level = args.level
        if args.skip:
            Config.skip_input = args.skip
        if args.time:
            Config.delay = args.time
