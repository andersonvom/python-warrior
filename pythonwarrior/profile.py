from level import Level


class Profile(object):

    tower_path = None
    player_path = None
    warrior_name = None
    level_number = None
    directory_name = None

    def __init__(self):
        print "TODO: Profile#__init__"
        self.level_number = 0

    def calculate_average_grade(self):
        print "TODO: Profile#calculate_average_grade"

    def epic(self):
        print"TODO: Profile#epic"

    def current_level(self):
        return Level(self, self.level_number)

    @classmethod
    def load(cls, profile):
        print "TODO: Profile#load"
