__author__ = 'kevin'


class Stack():

    def __init__(self):
        self._collection = list()

    def push(self, data):
        self._collection.append(data)

    def pop(self):
        return self._collection.pop()

    @property
    def top(self):
        return self._collection[-1]