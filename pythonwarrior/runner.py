from pythonwarrior.game import Game


class Runner(object):
    def __init__(self, arguments, stdin, stdout):
        self.arguments = arguments
        self.stdin = stdin
        self.stdout = stdout
        self.game = Game()

    def run(self):
        self.game.start()
