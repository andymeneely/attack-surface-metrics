__author__ = 'kevin'


class BaseFormatter(object):

    def __init__(self, call_graph):
        """Constructor for BaseFormatter"""
        self.call_graph = call_graph

    def write_output(self):
        pass