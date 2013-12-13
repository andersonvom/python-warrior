import io
import mock
import unittest

import pythonwarrior


class TestUI(unittest.TestCase):
    def setUp(self):
        self.ui = pythonwarrior.UI
        self.config = pythonwarrior.Config
        self.config.reset()
        self._out = io.StringIO()
        self._in = io.StringIO()
        self.config.out_stream = self._out
        self.config.in_stream = self._in

    def test_writeline_write_to_out_stream_with_newline(self):
        self.ui.writeline("foo")
        self.assertEqual('foo\n', self._out.getvalue())

    def test_write_writes_to_out_stream(self):
        self.ui.write('foo')
        self.assertEqual('foo', self._out.getvalue())

    def test_readline_reads_from_in_stream(self):
        self._in.write(unicode('foo\n'))
        self._in.seek(0)
        self.assertEqual('foo', self.ui.readline())

    def test_readline_returns_empty_string_on_no_input(self):
        self.config.in_stream = None
        self.assertEqual('', self.ui.readline())

    def test_request_text_input(self):
        self._in.write(unicode('bar'))
        self._in.seek(0)

        self.assertEqual('bar', self.ui.request('foo'))
        self.assertEqual('foo', self._out.getvalue())

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_ask_for_yes_or_no(self, mock_request):
        self.ui.ask('foo?')
        self.ui.request.assert_called_once_with('foo? [yn] ')

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_ask_returns_true_when_yes(self, mock_request):
        mock_request.return_value = 'y'
        self.assertEqual(True, self.ui.ask('foo?'))

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_ask_returns_false_when_no(self, mock_request):
        mock_request.return_value = 'n'
        self.assertEqual(False, self.ui.ask('foo?'))

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_ask_returns_false_for_any_input(self, mock_request):
        mock_request.return_value = 'xkcd'
        self.assertEqual(False, self.ui.ask('foo?'))

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_choose_shows_options_and_returns_selected_one(self, mock_request):
        options = ['foo', 'bar', 'baz']
        mock_request.return_value = '2'

        response = self.ui.choose('item', options)
        message = mock_request.call_args[0][0]
        self.assertIn('item', message)
        self.assertEqual('bar', response)
        self.assertIn('[1] foo', self._out.getvalue())
        self.assertIn('[2] bar', self._out.getvalue())
        self.assertIn('[3] baz', self._out.getvalue())

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_choose_accepts_arrays_as_options(self, mock_request):
        options = ['foo', 'bar', ['tower', 'easy']]
        mock_request.return_value = '3'

        self.ui.choose('item', options)
        self.assertIn('[3] easy', self._out.getvalue())

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_choose_returns_option_if_only_one(self, mock_request):
        options = ['foo']
        mock_request.return_value = '3'
        self.config.in_stream = mock.Mock()
        self.config.out_stream = mock.Mock()

        response = self.ui.choose('item', options)
        self.assertEqual('foo', response)
        self.assertEqual(False, mock_request.called)
        self.assertEqual(False, self.config.in_stream.called)
        self.assertEqual(False, self.config.out_stream.called)

    @mock.patch.object(pythonwarrior.UI, 'request')
    def test_choose_returns_value_if_option_is_array(self, mock_request):
        options = [['foo', 'bar']]
        self.assertEqual('foo', self.ui.choose('item', options))

    @mock.patch.object(pythonwarrior.ui.time, 'sleep')
    @mock.patch.object(pythonwarrior.UI, 'writeline')
    def test_writeline_with_delay(self, mock_writeline, mock_sleep):
        self.config.delay = 1.3
        self.ui.writeline_with_delay('foo')
        mock_writeline.assert_called_once_with('foo')
        mock_sleep.assert_called_once_with(1.3)

    @mock.patch.object(pythonwarrior.ui.time, 'sleep')
    @mock.patch.object(pythonwarrior.UI, 'writeline')
    def test_writeline_with_delay_no_delay(self, mock_writeline, mock_sleep):
        self.config.delay = None
        self.ui.writeline_with_delay('foo')
        mock_writeline.assert_called_once_with('foo')
        self.assertEqual(False, mock_sleep.called)
