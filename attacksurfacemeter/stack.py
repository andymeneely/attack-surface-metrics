__author__ = 'kevin'


class Stack():
    """
        Simple Stack (FILO collection) implementation based on python's list.
    """

    def __init__(self):
        """
            Stack constructor.

            Returns:
                A new instance of Stack.
        """
        self._collection = list()

    def __len__(self):
        """
            Returns the number of objects contained in the Stack.

            Returns:
                An Int representing the number of objects contained in the Stack.
        """
        return len(self._collection)

    def push(self, data):
        """
            Adds an object at the top of the Stack.

            Args:
                data: The object that will be added at the top of the Stack.
        """
        self._collection.append(data)

    def pop(self):
        """
            Removes the object at the top of the Stack and returns it.

            Returns:
                The object at the top of the Stack.
        """
        return self._collection.pop()

    @property
    def top(self):
        """
            Returns the object at the top of the Stack.
        """
        if self._collection:
            return self._collection[-1]
        else:
            return None