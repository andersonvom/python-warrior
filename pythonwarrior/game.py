import glob
import os
import sys

from config import Config
from level import Level
from profile import Profile
from tower import Tower
from ui import UI


class Game(object):

    _profile = None
    _current_level = None
    _next_level = None

    def start(self):
        UI.writeline("Welcome to Python Warrior")

        profile = Config.get('path_prefix') + '/.profile'
        game_directory = Config.get('path_prefix') + '/pythonwarrior'
        if os.path.exists(profile):
            self._profile = Profile.load(profile)
        elif not os.path.exists(game_directory):
            self.make_game_directory()

        if self.profile().epic():
            if self.profile().level_after_epic():
                self.go_back_to_normal_mode()
            else:
                self.play_epic_mode()
        else:
            self.play_normal_mode()

    def make_game_directory(self):
        question = "No pythonwarrior directory found. " \
                   "Would you like to create one?"
        if UI.ask(question):
            os.makedirs(Config.get('path_prefix') + '/pythonwarrior')
        else:
            UI.writeline("Unable to continue without a directory.")
            sys.exit(1)

    def play_normal_mode(self):
        print "TODO: Game#play_normal_mode"

    # PROFILES

    def profile_paths(self):
        location = Config.get('path_prefix') + '/pythonwarrior/**/.profile'
        return glob.glob(location)

    def profiles(self):
        return map(Profile.load, self.profile_paths())

    def profile(self):
        if not self._profile:
            self._profile = self._choose_profile()

        return self._profile

    def new_profile(self):
        profile = Profile()
        profile.tower_path = UI.choose('tower', self.towers()).path
        profile.warrior_name = UI.request('Enter a name for your warrior: ')

        return profile

    def _verify_profile_replacement(self, profile):
        replace_question = "Are you sure you want to replace your " \
                           "existing profile for this tower?"
        if UI.ask(replace_question):
            UI.writeline("Replacing existing profile")
        else:
            UI.writeline("Not replacing profile.")
            sys.exit(1)

    def _choose_profile(self):
        current_profiles = self.profiles() + [['new', 'New Profile']]
        profile = UI.choose('profile', current_profiles)
        if profile == 'new':
            profile = self.new_profile()
            current_path = profile.player_path
            if any(p.player_path == current_path for p in self.profiles()):
                self._verify_profile_replacement(profile)

        return profile

    # TOWERS

    def towers(self):
        return map(Tower, self.tower_paths())

    def tower_paths(self):
        location = 'towers/*'
        return glob.glob(location)

    # LEVELS

    def current_level(self):
        if not self._current_level:
            self._current_level = self.profile().current_level()

        return self._current_level

    def next_level(self):
        if not self._next_level:
            self._next_level = self.profile().next_level()

        return self._next_level

    def final_report(self):
        report = ""
        average_grade = self.profile().calculate_average_grade()
        if average_grade and not Config.get('practice_level'):
            report += "Your average grade for this tower is: %s\n\n" % \
                      Level.grade_letter(average_grade)
            levels = self.profile().current_epic_grades.keys()
            for level in sorted(levels):
                grade = self.profile().current_epic_grades[level]
                grade_letter = Level.grade_letter(grade)
                report += "Level %s: %s\n" % (level, grade_letter)

            report += "\nTo practice a level, use -l option\n\n"
            report += "pythonwarrior -l 3"

        return report
