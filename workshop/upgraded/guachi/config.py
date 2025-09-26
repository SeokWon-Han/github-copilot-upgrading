from configparser import ConfigParser
from os.path import isfile

class DictMatch(object):
    def __init__(self, config=None, mapped_options=None, mapped_defaults=None):
        self.config = config
        self.mapped_options = mapped_options if mapped_options is not None else {}
        self.mapped_defaults = mapped_defaults if mapped_defaults is not None else {}

    def options(self):
        configuration = self.defaults()
        try:
            if self.config is None or not isfile(self.config):
                configuration = self.defaults()
                return configuration
        except TypeError:
            if isinstance(self.config, dict):
                configuration = self.key_matcher(self.config, return_empty=True)
                if not configuration:
                    configuration = self.defaults(self.config)
                return configuration
            else:
                configuration = self.key_matcher(self.config)
                return configuration
        else:
            try:
                parser = ConfigParser()
                parser.read(self.config)
                file_options = parser.defaults()
                configuration = self.key_matcher(file_options)
            except Exception as error:
                raise OptionConfigurationError(error)
        return configuration

    def key_matcher(self, original, return_empty=False):
        converted_opts = {}
        for key, value in self.mapped_options.items():
            try:
                file_value = original[key]
                converted_opts[value] = file_value
            except KeyError:
                pass
        if len(converted_opts) == 0 and return_empty:
            return False
        try:
            configuration = self.defaults(converted_opts)
            return configuration
        except Exception as error:
            raise OptionConfigurationError(error)

    def defaults(self, config=None):
        if config is None:
            return self.mapped_defaults.copy()
        for key in self.mapped_defaults.keys():
            try:
                if config[key] == '':
                    config[key] = self.mapped_defaults[key]
            except KeyError:
                config[key] = self.mapped_defaults[key]
        return config

class OptionConfigurationError(Exception):
    pass
