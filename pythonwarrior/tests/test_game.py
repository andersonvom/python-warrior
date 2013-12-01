import glob
import mock
import os
import unittest

import pythonwarrior


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = pythonwarrior.Game()

    # GAME DIR

    @mock.patch.object(os, 'makedirs')
    @mock.patch.object(pythonwarrior.UI, 'ask')
    def test_creates_new_directory_if_player_says_so(self, mock_ask,
                                                     mock_makedirs):
        mock_ask.return_value = True

        self.game.make_game_directory()
        mock_makedirs.assert_called_once_with('./pythonwarrior')

    @mock.patch.object(os, 'makedirs')
    @mock.patch.object(pythonwarrior.UI, 'ask')
    def test_doesnt_create_game_and_exit_if_player_says_no(self, mock_ask,
                                                           mock_makedirs):
        mock_ask.return_value = False
        mock_makedirs.side_effect = Exception('should not be called')

        self.assertRaises(SystemExit, self.game.make_game_directory)

    # PROFILES

    @mock.patch.object(pythonwarrior.Profile, 'load')
    def test_loads_profiles_for_each_profile_path(self, mock_load):
        def mock_load_values(path):
            mapping = {
                'foo/.profile': 1,
                'bar/.profile': 2,
            }
            return mapping[path]

        mock_load.side_effect = mock_load_values
        self.game.profile_paths = mock.Mock()
        self.game.profile_paths.return_value = ['foo/.profile', 'bar/.profile']

        self.assertEquals([1, 2], self.game.profiles())

    @mock.patch.object(glob, 'glob')
    def test_find_profile_paths(self, mock_glob):
        self.game.profile_paths()
        mock_glob.assert_called_once_with('./pythonwarrior/**/.profile')

    def test_creates_profile_when_no_profile_path_is_specified(self):
        new_profile = mock.Mock(name='p1')
        self.game.new_profile = mock.Mock(return_value=new_profile)

        self.assertEquals(new_profile, self.game.profile())
        self.game.new_profile.assert_called_once()

    @mock.patch.object(pythonwarrior.UI, 'choose')
    def test_asks_once_to_choose_profile_if_available(self, mock_choose):
        self.game.profiles = mock.Mock(return_value=['p1'])

        self.game.profile()
        self.game.profile()
        mock_choose.assert_called_once()

    @mock.patch.object(pythonwarrior.UI, 'choose')
    @mock.patch.object(pythonwarrior.UI, 'gets')
    def test_asks_user_to_choose_tower_on_new_profile(self, mock_gets,
                                                      mock_choose):
        mock_gets.return_value = ''
        self.game.towers = mock.Mock(return_value=['t1', 't2'])
        fake_tower = mock.Mock()
        fake_tower.path = '/foo/bar'

        self.game.new_profile()
        mock_choose.assert_called_once_with('tower', ['t1', 't2'])

    @mock.patch.object(pythonwarrior.UI, 'request')
    @mock.patch.object(pythonwarrior.UI, 'choose')
    def test_pass_name_and_tower_to_profile(self, mock_choose, mock_request):
        mock_choose.return_value = mock.Mock(path='tower_path')
        mock_request.return_value = 'name'

        profile = self.game.new_profile()
        self.assertEquals('tower_path', profile.tower_path)
        self.assertEquals('name', profile.warrior_name)
