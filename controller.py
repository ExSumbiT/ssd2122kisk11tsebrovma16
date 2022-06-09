from models import Sequence, Parser
from json import loads
from XmlDict import xml_to_dict, XmlDictConfig
from random import randint, sample
import csv


def print_(func):
    def inner(*args, **kwargs):
        sequence = func(*args, **kwargs)
        print_items(sequence)
    return inner


def print_items(sequence):
    for idx, sequence in enumerate(sequence):
        print(f'{idx + 1}. ', end='')
        for (k, v) in sequence.items():
            print(f'{k}: {v}', end=' | ')
        print('\n', end='')


class Controller:

    def __init__(self):
        self.sequences = []
        self.current_sequence = None

    def print_sequences(self):
        if self.sequences:
            for sequence in self.sequences:
                print(sequence)
        else:
            print('<empty>')

    def print_sequence(self, index):
        print_items(self.sequences[int(index)-1])

    def print_active(self):
        self.print_sequence(self.sequences.index(self.current_sequence)-1)

    def set_active(self, index):
        self.current_sequence = self.sequences[int(index)-1]
        self.print_active()

    def load_file(self, filename):
        items = xml_to_dict(filename)
        self.load_sequence(seq_list=items)

    @print_
    def load_sequence(self, sequence=None, seq_list=None):
        seq = Sequence()
        self.sequences.append(seq)
        self.current_sequence = seq
        if sequence:
            item = loads(sequence)
            if type(item) == list:
                self.list_to_sequence(seq, item)
            elif type(item) == dict:
                self.dict_to_sequence(seq, item, index='up')
        if seq_list:
            self.list_to_sequence(seq, seq_list)
        return self.current_sequence

    def get_element(self, number: int):
        print(self.current_sequence[int(number)-1])

    def get_sequence(self, index):
        return self.sequences[int(index)-1]

    def list_to_sequence(self, seq, seq_list: list):
        for item in seq_list:
            self.dict_to_sequence(seq, item, index=seq_list.index(item)+1)

    def dict_to_sequence(self, seq, seq_dict: dict, index=None):
        if type(seq_dict) in [dict, XmlDictConfig]:
            if 'value' in seq_dict:
                try:
                    value = int(seq_dict['value'])
                    seq.add({'value': value})
                except:
                    print('Error: value not a number')
            else:
                print(f'Was expected <value> in sequence <{index}>')
        else:
            self.dict_to_sequence(seq, {'value': seq_dict})

    def random_sequence(self, number):
        self.load_sequence(seq_list=sample(range(0, 99), int(number)))

    def random_all(self):
        self.random_sequence(randint(1, 9))

    def export(self, filename='export'):
        with open(f'{filename}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for sequence in self.sequences:
                prepare = sequence.export()
                writer.writerow(prepare)
            print(f'Exported to {csvfile.name}')


class Calculator:

    def __init__(self, controller):
        self.controller = controller
        self.parser = Parser()
        self.seq_list = []
        self.max_len = 0
        self.expression = None

    def parse(self, expression):
        self.parser.set_expression(expression)
        self.expression = self.parser.parse()
        sequences = [self.controller.get_sequence(_) for _ in self.expression if _.isdigit()]
        for sequence in sequences:
            if len(sequence) > self.max_len:
                self.max_len = len(sequence)
        for i in range(self.max_len):
            new_expression = self.get_expression(i)
            self.calculate(new_expression)
        self.controller.load_sequence(seq_list=self.seq_list)
        self.seq_list = []

    def get_expression(self, idx):
        sequence_value = 0
        new_expression = []
        for index, c in enumerate(self.expression):
            if c.isdigit():
                try:
                    sequence_value = self.controller.get_sequence(c)[idx]
                except IndexError:
                    deny = (self.expression[index - 1], self.expression[index + 1])
                    if any(_ in deny for _ in ['*', '/']):
                        sequence_value = 1
                new_expression.append(str(sequence_value))
            else:
                new_expression.append(c)
        return new_expression

    def calculate(self, new_expression):
        print(new_expression)
        self.seq_list.append(int(eval(''.join(new_expression))))
