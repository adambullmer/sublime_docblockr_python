from abc import abstractmethod, ABCMeta

from .registry import register

def counter():
    """Simple Iteratable Counter.

    Starting from 0, will continue to give a new counter number every time
    this function is iterated over, or with the use of `next()`

    Yields:
        {Integer} Current Counter Number
    """
    count = 0
    while True:
        count += 1
        yield count


class FormatterMeta(type):
    def __new__(mcs, classname, bases, attributes):
        print('New Class')
        newclass = super(FormatterMeta, mcs).__new__(mcs, classname, bases, attributes)
        register(newclass)
        return newclass


class BaseFormatter(object):
    __metaclass__ = ABCMeta

    name = 'base'
    tab_index = None

    def __init__(self):
        self.tab_index = counter()

    def __dict__(self):
        return {
            'summary': self.summary(),
            'description': self.description(),
            'arguments': self.arguments(),
            'keyword_arguments': self.keyword_arguments(),
            'returns': self.returns(),
            'yields': self.yields(),
            'extends': self.extends(),
            'decorators': self.decorators(),
        }

    def __iter__(self):
        for attr, value in self.__dict__().items():
            yield attr, value

    def summary(self):
        return '${' + str(next(self.tab_index)) + ':[summary]}'

    def description(self):
        return '\n\n${' + str(next(self.tab_index)) + ':[description]}\n'

    @abstractmethod
    def decorators(self, attributes):
        return '${' + str(next(self.tab_index)) + ':[decorators]}\n'

    @abstractmethod
    def extends(self, attributes):
        return '${' + str(next(self.tab_index)) + ':[extends]}\n'

    @abstractmethod
    def arguments(self, attributes):
        return '${' + str(next(self.tab_index)) + ':[arguments]}\n'

    @abstractmethod
    def keyword_arguments(self, attributes):
        return '${' + str(next(self.tab_index)) + ':[keyword arguments]}\n'

    @abstractmethod
    def returns(self, attribute):
        return '${' + str(next(self.tab_index)) + ':[returns]}\n'

    @abstractmethod
    def yields(self, attribute):
        return '${' + str(next(self.tab_index)) + ':[yields]}\n'

    @abstractmethod
    def raises(self, attributes):
        return '${' + str(next(self.tab_index)) + ':[raises]}\n'

    @abstractmethod
    def variables(self, attributes):
        return '${' + str(next(self.tab_index)) + ':[variables]}\n'
