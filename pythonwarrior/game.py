import glob
import os
import sys

from config import Config
from profile import Profile
from tower import Tower
from ui import UI


class Game(object):

    _profile = None

    def start(self):
        print 'Game started'

    def make_game_directory(self):
        question = "No pythonwarrior directory found. " \
                   "Would you like to create one?"
        if UI.ask(question):
            os.makedirs(Config.get('path_prefix') + '/pythonwarrior')
        else:
            UI.puts("Unable to continue without a directory.")
            sys.exit(1)

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
            UI.puts("Replacing existing profile")
        else:
            UI.puts("Not replacing profile.")
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
        return map(Tower.__initialize__, self.tower_paths())

    def tower_paths(self):
        location = '../../../towers/*'
        return glob.glob(location)
