"""Base formatter class."""
from abc import abstractmethod, ABCMeta

from .registry import register


def counter():
    """Simple Iteratable Counter.

    Starting from 0, will continue to give a new counter number every time
    this function is iterated over, or with the use of `next()`

    Yields:
        {int} Current Counter Number
    """
    count = 0
    while True:
        count += 1
        yield count


class FormatterMeta(ABCMeta):
    """Register the class in the formatter.

    Extends:
        ABCMeta
    """

    def __new__(mcs, classname, bases, attributes):
        """---."""
        newclass = super(FormatterMeta, mcs).__new__(mcs, classname, bases, attributes)
        register(newclass)
        return newclass


class Base(metaclass=FormatterMeta):
    """Base Formatter Class.

    This class provides the template that all inheriting Formatters should follow.
    By using this base class, the formatter will be registered with the formatter
    registry and therefore usable. Apart from the abstract methods, there are some
    important convenience methods setup on the base class. It is also important to
    note that any inheriting class _must_ set the `name` variable if it wants to
    be registered in the registry.

    - _generate_field -- Generates tabbable snippet fields.
    - summary -- Generic summary line.
    - description -- Generic description line.

    Extends:
        metaclass=FormatterMeta

    Variables:
        name {str} -- The name the formatter will be registered under.
        tab_index {generator} -- Provides a simple count generator for convenience
                                 in making tabbable fields
    """

    name = None
    tab_index = counter()

    def __dict__(self):
        """---."""
        return {
            'summary': self.summary,
            'description': self.description,
            'decorators': self.decorators,
            'extends': self.extends,
            'arguments': self.arguments,
            'keyword_arguments': self.keyword_arguments,
            'returns': self.returns,
            'yields': self.yields,
            'raises': self.raises,
            'variables': self.variables,
        }

    def __iter__(self):
        """---."""
        for attr, value in self.__dict__().items():
            yield attr, value

    def _generate_field(self, name, value=None):
        """Make a Sublime Text snippet field.

        If a value is passed and it is not None, it will be returned. Otherwise,
        this will generate a snippet field in the next tabbable index.

        Arguments:
            name {str} -- Name of the placeholder text

        Keyword Arguments:
            value {str} -- Text to replace the field if not None (default: {None})

        Returns:
            str -- Snippet Field
        """
        if value is not None:
            return value

        return '${{{tab_index}:[{name}]}}'.format(
            tab_index=next(self.tab_index),
            name=name
        )

    def summary(self):
        """Create snippet string for the summary line."""
        return '{}'.format(self._generate_field('summary'))

    def description(self):
        """Create snippet string for the description body."""
        return '\n\n{}\n'.format(self._generate_field('description'))

    @abstractmethod
    def decorators(self, attributes):
        """Create snippet string for a list of decorators."""
        return ''

    @abstractmethod
    def extends(self, attributes):
        """Create snippet string for a list of extended objects."""
        return ''

    @abstractmethod
    def arguments(self, attributes):
        """Create snippet string for a list of arguments."""
        return ''

    @abstractmethod
    def keyword_arguments(self, attributes):
        """Create snippet string for a list of keyword arguments."""
        return ''

    @abstractmethod
    def returns(self, attribute):
        """Create snippet string for a list of return values."""
        return ''

    @abstractmethod
    def yields(self, attribute):
        """Create snippet string for a list of yielded results."""
        return ''

    @abstractmethod
    def raises(self, attributes):
        """Create snippet string for a list of raiased exceptions."""
        return ''

    @abstractmethod
    def variables(self, attributes):
        """Create snippet string for a list of variables."""
        return ''


class BaseFormatter(Base):
    """Documentation Formatter Class."""

    def decorators(self, attributes):
        """Create snippet string for a list of decorators."""
        return '{}\n'.format(self._generate_field('decorators'))

    def extends(self, attributes):
        """Create snippet string for a list of extended objects."""
        return '{}\n'.format(self._generate_field('extends'))

    def arguments(self, attributes):
        """Create snippet string for a list of arguments."""
        return '{}\n'.format(self._generate_field('arguments'))

    def keyword_arguments(self, attributes):
        """Create snippet string for a list of keyword arguments."""
        return '{}\n'.format(self._generate_field('keyword arguments'))

    def returns(self, attribute):
        """Create snippet string for a list of return values."""
        return '{}\n'.format(self._generate_field('returns'))

    def yields(self, attribute):
        """Create snippet string for a list of yielded results."""
        return '{}\n'.format(self._generate_field('yields'))

    def raises(self, attributes):
        """Create snippet string for a list of raiased exceptions."""
        return '{}\n'.format(self._generate_field('raises'))

    def variables(self, attributes):
        """Create snippet string for a list of variables."""
        return '{}\n'.format(self._generate_field('variables'))
