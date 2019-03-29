"""test config module"""
import os
from configparser import ConfigParser
import unittest

import searchstims.config


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(
            HERE, '..', 'src', 'searchstims', 'config', 'default.ini'
)


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_configs = os.path.join(HERE, 'test_data', 'configs')
        self.default_config = ConfigParser()
        self.default_config.read(DEFAULT_CONFIG_FILE)

    def test_parse_rectangle_config(self):
        # get file we need and load into ConfigParser instance to use for tests
        rectangle_config_file = os.path.join(self.test_configs, 'rectangle_config.ini')
        rectangle_config = ConfigParser()
        rectangle_config.read(rectangle_config_file)
        rectangle_config_obj = searchstims.config.parse(rectangle_config_file)

        self.assertTrue(hasattr(rectangle_config_obj, 'general'))
        self.assertTrue(hasattr(rectangle_config_obj, 'rectangle'))
        self.assertTrue(rectangle_config_obj.number is None)

    def test_parse_number_config(self):
        # get file we need and load into ConfigParser instance to use for tests
        number_config_file = os.path.join(self.test_configs, 'number_config.ini')
        number_config = ConfigParser()
        number_config.read(number_config_file)
        number_config_obj = searchstims.config.parse(number_config_file)

        self.assertTrue(hasattr(number_config_obj, 'general'))
        self.assertTrue(hasattr(number_config_obj, 'number'))
        self.assertTrue(number_config_obj.rectangle is None)


if __name__ == '__main__':
    unittest.main()
