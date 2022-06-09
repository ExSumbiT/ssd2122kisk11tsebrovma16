import itertools


class Sequence:
    id_iter = itertools.count(1)

    def __init__(self, *args, **kwargs):
        self.id = next(self.id_iter)
        self.items = list()

    def __iter__(self):
        return SequenceIterator(self)

    def __getitem__(self, i):
        return self.items[i]['value']

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f'{self.id}. Items: {self.__len__()}'

    def add(self, item):
        if type(item) == dict:
            self.items.append(item)
        else:
            self.add({'value': item})

    def export(self):
        return [d['value'] for d in self.items]


class SequenceIterator:
    """Iterator class"""

    def __init__(self, sequence):
        # Sequence object reference
        self._sequence = sequence
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """ Returns the next value from sequence object's lists """
        if self._index < (len(self._sequence.items)):
            result = self._sequence.items[self._index]
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration


class Parser:

    def __init__(self, expression=None):
        self.expression = expression

    def set_expression(self, expression):
        self.expression = expression

    def parse(self):
        num_out = []  # this holds the non-operators that are found in the string (left to right)
        buff = []
        for c in self.expression:
            buff.append(c)
        num_out.append(''.join(buff))
        return buff
