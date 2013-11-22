import unittest

from pythonwarrior.config import Config


class TestConfig(unittest.TestCase):
    def test_reset_sets_all_class_variables_to_none(self):
        Config.delay = 'fake delay'
        Config.in_stream = 'fake instream'
        Config.out_stream = 'fake outstream'
        Config.practice_level = 'fake practive_level'
        Config.path_prefix = 'fake path_prefix'
        Config.skip_input = 'fake skip_input'

        Config.reset()

        self.assertEquals(None, Config.delay)
        self.assertEquals(None, Config.in_stream)
        self.assertEquals(None, Config.out_stream)
        self.assertEquals(None, Config.practice_level)
        self.assertEquals(None, Config.path_prefix)
        self.assertEquals(None, Config.skip_input)

    def test_get_returns_class_attributes(self):
        Config.foo = 'bar'
        self.assertEquals('bar', Config.get('foo'))
        delattr(Config, 'foo')

    def test_get_returns_default_values_if_not_set(self):
        Config.foo = None
        Config._defaults['foo'] = 'baz'
        self.assertEquals('baz', Config.get('foo'))
        delattr(Config, 'foo')
