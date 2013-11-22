import os
import sys

from config import Config
from ui import UI


class Game(object):
    def start(self):
        print 'Game started'

    def make_game_directory(self):
        question = "No pythonwarrior directory found. " \
                   "Would you like to create one?"
        if UI.ask(question):
            os.makedirs(Config.get('path_prefix') + '/pythonwarrior')
        else:
            UI.puts("Unable to continue without a directory.")
            sys.exit()
