from guachi.database import dbdict
from guachi.config import DictMatch
import os

class ConfigMapper(object):
    def __init__(self, path):
        self.path = self._path_verify(path)

    def __call__(self):
        db = dbdict(self.path)
        return db

    def set_ini_options(self, dictionary):
        db = dbdict(self.path, table='_guachi_options')
        for key, value in dictionary.items():
            db[key] = value

    def set_default_options(self, dictionary):
        db = dbdict(self.path, table='_guachi_defaults')
        for key, value in dictionary.items():
            db[key] = value

    def get_ini_options(self):
        db = dbdict(self.path, table='_guachi_options')
        return db

    def get_default_options(self):
        db = dbdict(self.path, table='_guachi_defaults')
        return db

    def set_config(self, configuration=None):
        mapped_ini = self.get_ini_options()
        mapped_defaults = self.get_default_options()
        dict_match = DictMatch(configuration, mapped_ini, mapped_defaults)
        dict_config = dict_match.options()
        if len(dict_config.items()) > 0:
            db = dbdict(self.path)
            for key, value in dict_config.items():
                db[key] = value

    def update_config(self, configuration=None):
        return self.set_config(configuration)

    def _path_verify(self, path):
        if os.path.isdir(path):
            return os.path.join(path, 'guachi.db')
        return path

    def stored_config(self):
        db = dbdict(self.path)
        return db.get_all()

    def get_dict_config(self):
        db = dbdict(self.path)
        return db.get_all()

    def _integrity_check(self):
        db = dbdict(self.path)
        return db._integrity_check()
