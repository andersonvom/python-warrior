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

    # TOWERS

    @mock.patch.object(pythonwarrior.Tower, '__initialize__')
    def test_load_towers_for_each_tower_path(self, mock_init):
        def mock_new(arg):
            return {
                'towers/foo': 1,
                'towers/bar': 2,
            }[arg]

        mock_init.side_effect = mock_new
        tower_paths = ['towers/foo', 'towers/bar']
        self.game.tower_paths = mock.Mock(return_value=tower_paths)

        towers = self.game.towers()
        self.assertIn(1, towers)
        self.assertIn(1, towers)
        self.assertEquals(2, len(towers))

    @mock.patch.object(glob, 'glob')
    def test_find_tower_paths(self, mock_glob):
        self.game.tower_paths()
        mock_glob.assert_called_once_with('../../../towers/*')

    # LEVEL

    def test_fetch_current_level_from_profile_and_cache_it(self):
        profile = mock.Mock()
        profile.current_level.return_value = 'foo'
        self.game.profile = mock.Mock(return_value=profile)

        self.assertEquals('foo', self.game.current_level())
        profile.current_level.return_value = 'not foo'
        self.assertEquals('foo', self.game.current_level())

    def test_fetch_next_level_from_profile_and_cache_it(self):
        profile = mock.Mock()
        profile.next_level.return_value = 'foo'
        self.game.profile = mock.Mock(return_value=profile)

        self.assertEquals('foo', self.game.next_level())
        profile.next_level.return_value = 'not foo'
        self.assertEquals('foo', self.game.next_level())

    @mock.patch.object(pythonwarrior.Level, 'grade_letter')
    def test_reports_final_grade(self, mock_grade_letter):
        def _mock_grade_letter(arg):
            return {
                '0.7': 'C',
                '0.8': 'B',
                '0.9': 'A',
            }[str(arg)]

        mock_grade_letter.side_effect = _mock_grade_letter
        profile = mock.Mock()
        profile.current_epic_grades = {1: 0.7, 2: 0.9}
        profile.calculate_average_grade.return_value = 0.8
        self.game.profile = mock.Mock(return_value=profile)

        report = self.game.final_report()
        self.assertIn("Your average grade for this tower is: B", report)
        self.assertIn("Level 1: C", report)
        self.assertIn("Level 2: A", report)

    def test_final_report_is_empty_if_no_epic_grades(self):
        profile = mock.Mock()
        profile.calculate_average_grade.return_value = None
        self.game.profile = mock.Mock(return_value=profile)

        self.assertEquals('', self.game.final_report())

    @mock.patch.object(pythonwarrior.Config, 'practice_level')
    def test_final_report_is_emtpy_if_practice_level(self, mock_level):
        pythonwarrior.Config.practice_level = 2
        profile = mock.Mock()
        profile.current_epic_grades = {1: 0.7, 2: 0.9}
        profile.calculate_average_grade.return_value = 0.8
        self.game.profile = mock.Mock(return_value=profile)

        self.assertEquals('', self.game.final_report())
