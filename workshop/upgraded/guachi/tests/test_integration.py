from os import path, remove, mkdir
import unittest
from guachi import ConfigMapper

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.mapped_options = {
            'guachi.db.host': 'db_host',
            'guachi.db.port': 'db_port',
            'guachi.web.host': 'web_host',
            'guachi.web.port': 'web_port',
        }
        self.mapped_defaults = {
            'db_host': 'localhost',
            'db_port': 27017,
            'web_host': 'localhost',
            'web_port': 8080,
        }
        try:
            if path.exists('/tmp/guachi'):
                remove('/tmp/guachi')
            else:
                mkdir('/tmp/guachi')
        except Exception:
            pass

    def tearDown(self):
        try:
            if path.exists('/tmp/guachi'):
                remove('/tmp/guachi')
            else:
                mkdir('/tmp/guachi')
        except Exception:
            pass

    def test_access_mapped_configs_empty_dict(self):
        foo = ConfigMapper('/tmp/guachi')
        foo.set_ini_options(self.mapped_options)
        foo.set_default_options(self.mapped_defaults)
        foo.set_config({})
        self.assertEqual(foo(), {})
        self.assertEqual(foo.path, '/tmp/guachi/guachi.db')
        self.assertEqual(foo.get_ini_options(), {})
        self.assertEqual(foo.get_default_options(), {})
        self.assertEqual(foo.get_dict_config(), self.mapped_defaults)
        self.assertEqual(foo.stored_config(), self.mapped_defaults)
        self.assertTrue(foo._integrity_check())

    def test_access_mapped_configs_dict(self):
        foo = ConfigMapper('/tmp/guachi')
        foo.set_ini_options(self.mapped_options)
        foo.set_default_options(self.mapped_defaults)
        foo.set_config({'db_host': 'example.com', 'db_port': 0})
        self.assertEqual(foo(), {})
        self.assertEqual(foo.path, '/tmp/guachi/guachi.db')
        self.assertEqual(foo.get_ini_options(), {})
        self.assertEqual(foo.get_default_options(), {})
        expected = {
            'web_port': 8080,
            'web_host': 'localhost',
            'db_host': 'example.com',
            'db_port': 0
        }
        self.assertEqual(foo.get_dict_config(), expected)
        self.assertEqual(foo.stored_config(), expected)
        self.assertTrue(foo._integrity_check())
