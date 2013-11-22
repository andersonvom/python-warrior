import mock
import sys
import unittest

import pythonwarrior
from pythonwarrior.runner import Runner


class TestRunner(unittest.TestCase):
    def setUp(self):
        pythonwarrior.Config.reset()
        self.runner = Runner([])

    def test___init__defaults_to_stdin_and_stdout(self):
        self.assertEquals(sys.stdin, self.runner.stdin)
        self.assertEquals(sys.stdout, self.runner.stdout)

    def test___init__accepts_different_in_out_streams(self):
        self.runner = Runner([], 'fake stdin', 'fake stdout')

        self.assertEquals('fake stdin', self.runner.stdin)
        self.assertEquals('fake stdout', self.runner.stdout)

    def test___init___accepts_command_line_arguments(self):
        self.runner = Runner(['pythonwarrior', 'fakearg'])

        self.assertEquals(['fakearg'], self.runner.arguments)
        self.assertEquals(True,
                          isinstance(self.runner.game, pythonwarrior.Game))

    def test___init___creates_a_new_game(self):
        self.assertEquals(True,
                          isinstance(self.runner.game, pythonwarrior.Game))

    def test_run_parses_command_line_options(self):
        self.runner.parse_options = mock.Mock()
        self.runner.run()

        self.runner.parse_options.assert_called_once_with()

    def test_run_sets_up_config_options(self):
        self.runner = Runner([], 'fake stdin', 'fake stdout')
        self.runner.run()

        self.assertEquals('fake stdin', pythonwarrior.Config.in_stream)
        self.assertEquals('fake stdout', pythonwarrior.Config.out_stream)
        self.assertEquals(0.6, pythonwarrior.Config.delay)

    def test_run_starts_the_game(self):
        self.runner.game = mock.Mock()
        self.runner.run()

        self.runner.game.start.assert_called_once_with()

    def test_parse_options_accepts_directory(self):
        self.runner = Runner(['pythonwarrior', '-d', 'fakevalue'])
        self.runner.parse_options()
        self.assertEquals('fakevalue', pythonwarrior.Config.path_prefix)

        self.runner = Runner(['pythonwarrior', '--directory', 'fakevalue'])
        self.runner.parse_options()
        self.assertEquals('fakevalue', pythonwarrior.Config.path_prefix)

    def test_parse_options_accepts_integer_levels(self):
        self.runner = Runner(['pythonwarrior', '-l', '42'])
        self.runner.parse_options()
        self.assertEquals(42, pythonwarrior.Config.practice_level)

        self.runner = Runner(['pythonwarrior', '--level', '42'])
        self.runner.parse_options()
        self.assertEquals(42, pythonwarrior.Config.practice_level)

    @mock.patch.object(sys, 'stderr')
    def test_parse_options_errors_on_non_int_levels(self, mock_stderr):
        self.runner = Runner(['pythonwarrior', '-l', '4.2'])
        self.assertRaises(SystemExit, self.runner.parse_options)

    def test_parse_options_accepts_skip(self):
        self.runner = Runner(['pythonwarrior', '-s'])
        self.runner.parse_options()
        self.assertEquals(True, pythonwarrior.Config.skip_input)

        self.runner = Runner(['pythonwarrior', '--skip'])
        self.runner.parse_options()
        self.assertEquals(True, pythonwarrior.Config.skip_input)

    def test_parse_options_accepts_float_time(self):
        self.runner = Runner(['pythonwarrior', '-t', '4.2'])
        self.runner.parse_options()
        self.assertEquals(4.2, pythonwarrior.Config.delay)

        self.runner = Runner(['pythonwarrior', '--time', '4.2'])
        self.runner.parse_options()
        self.assertEquals(4.2, pythonwarrior.Config.delay)

    @mock.patch.object(sys, 'stderr')
    def test_parse_options_errors_on_non_float_times(self, mock_stderr):
        self.runner = Runner(['pythonwarrior', '-l', 'nonfloat'])
        self.assertRaises(SystemExit, self.runner.parse_options)
