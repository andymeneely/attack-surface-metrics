__author__ = 'kevin'


class BaseLineParser(object):
    """"""
    _instance = None

    @staticmethod
    def get_instance():
        pass

    @staticmethod
    def _lazy_load_instance(constructor):
        if BaseLineParser._instance is None:
            BaseLineParser._instance = constructor()

        return BaseLineParser._instance

    def __init__(self):
        """"""
        self._function_name = ""
        self._function_signature = ""

    def load(self, line):
        pass

    def get_function_name(self, line=None):
        self._load_if_new(line)
        return self._function_name

    def get_function_signature(self, line=None):
        self._load_if_new(line)
        return self._function_signature

    def _load_if_new(self, line):
        if line is not None:
            self.load(line)