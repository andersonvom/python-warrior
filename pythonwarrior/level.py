class Level(object):

    number = None
    profile = None

    def __init__(self, profile, number):
        print "TODO: Level#__init__"
        self.profile = profile
        self.number = 0

    @classmethod
    def grade_letter(cls, grade):
        print "TODO: Level#grade_letter"
        pass
