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
