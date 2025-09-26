import unittest
import shutil
from os import remove, mkdir, path
from guachi.config import DictMatch, OptionConfigurationError

class MockDict(dict):
    pass

def create_configs():
    try:
        if path.exists('/tmp/guachi'):
            remove('/tmp/guachi')
        else:
            mkdir('/tmp/guachi')
    except Exception:
        pass
    txt = open('/tmp/guachi/conf.ini', 'w')
    text = """
[DEFAULT]
guachi.middleware.server_id = 2
guachi.middleware.application = secondary
guachi.db.host = remote.example.com
guachi.db.port = 00000
guachi.web.host = web.example.com
guachi.web.port = 80
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s %(message)s
guachi.cache = 10
"""
    txt.write(text)
    txt.close()

class TestDictMatch(unittest.TestCase):
    def test_defaults(self):
        defaults = {'a': 1, 'b': 2}
        dm = DictMatch(config=None, mapped_options={}, mapped_defaults=defaults)
        self.assertEqual(dm.defaults(), defaults)
