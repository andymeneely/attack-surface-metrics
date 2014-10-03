__author__ = 'kevin'


class BaseLoader(object):
    def load_call_graph(self):
        pass

    @property
    def error_messages(self):
        return list()