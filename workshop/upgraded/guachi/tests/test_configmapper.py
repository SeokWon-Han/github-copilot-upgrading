import os
import unittest
from guachi import ConfigMapper
from guachi.database import dbdict

DEFAULT_CONFIG = {
    'frequency': 60,
    'master': 'False',
    'host': 'localhost',
    'ssh_user': 'root',
    'ssh_port': 22,
    'hosts_path': '/opt/pacha',
    'hg_autocorrect': 'True',
    'log_enable': 'False',
    'log_path': 'False',
    'log_level': 'DEBUG',
    'log_format': '%(asctime)s %(levelname)s %(name)s %(message)s',
    'log_datefmt': '%H:%M:%S'
}

class TestConfigMapper(unittest.TestCase):
    def setUp(self):
        for dbfile in ['/tmp/guachi.db', '/tmp/foo_guachi.db']:
            try:
                os.remove(dbfile)
            except Exception:
                pass

    def tearDown(self):
        for dbfile in ['/tmp/guachi.db', '/tmp/foo_guachi.db']:
            try:
                os.remove(dbfile)
            except Exception:
                pass

    def test_init(self):
        foo = ConfigMapper('/tmp')
        expected = '/tmp/guachi.db'
        actual = foo.path
        self.assertEqual(actual, expected)

    def test__call__(self):
        foo = ConfigMapper('/tmp')
        actual = foo()
        expected = {}
        self.assertEqual(actual, expected)

    def test_set_ini_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'config.db.port': 'db_port'}
        foo.set_ini_options(my_config)
        db = dbdict(path='/tmp/guachi.db', table='_guachi_options')
        expected = my_config
        actual = db.get_all()
        self.assertEqual(actual, expected)

    def test_set_default_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'db_port': 1234}
        foo.set_default_options(my_config)
        db = dbdict(path='/tmp/guachi.db', table='_guachi_defaults')
        expected = my_config
        actual = db.get_all()
        self.assertEqual(actual, expected)

    def test_get_ini_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'config.db.port': 'db_port'}
        foo.set_ini_options(my_config)
        defaults = foo.get_ini_options()
        actual = defaults['config.db.port']
        expected = 'db_port'
        self.assertEqual(actual, expected)

    def test_get_default_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'db_port': 1234}
        foo.set_default_options(my_config)
        defaults = foo.get_default_options()
        actual = defaults['db_port']
        expected = 1234
        self.assertEqual(actual, expected)

    def test_path_verify_file(self):
        foo = ConfigMapper('/tmp/foo_guachi.db')
        actual = foo._path_verify('/tmp/foo_guachi.db')
        expected = '/tmp/foo_guachi.db'
        self.assertEqual(actual, expected)
