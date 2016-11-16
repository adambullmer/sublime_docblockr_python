"""Default Formatter for Numpy."""
from .base import Base


class NumpyFormatter(Base):
    """Documentation Formatter Class."""

    name = 'numpy'

    def decorators(self, attributes):
        """Create snippet string for a list of decorators."""
        return ''

    def extends(self, attributes):
        """Create snippet string for a list of extended objects."""
        return ''

    def arguments(self, attributes):
        """Create snippet string for a list of arguments."""
        section = '\nParameters\n----------\n'
        template = '{name} : {{{type}}}\n\t{description}\n'

        for attr in attributes['arguments']:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                type=self._generate_field('type', attr['type']),
                description=self._generate_field('description'),
            )

        section += self.keyword_arguments(attributes['keyword_arguments'])

        if len(attributes['arguments']) == 0 and len(attributes['keyword_arguments']) == 0:
            section = ''

        return section

    def keyword_arguments(self, attributes):
        """Create snippet string for a list of keyword arguments."""
        section = ''
        template = '{name} : {{{type}}}, optional\n\t{description} '\
                   '(the default is {default}, which {default_description})\n'

        if len(attributes) == 0:
            return ''

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                type=self._generate_field('type', attr['type']),
                description=self._generate_field('description'),
                default=self._generate_field('default', attr['default']),
                default_description=self._generate_field('default_description'),
            )

        return section

    def returns(self, attribute):
        """Create snippet string for a list of return values."""
        section = '\nReturns\n-------\n'
        template = '{type}\n\t{description}\n'

        section += template.format(
            type=self._generate_field('type', attribute['type']),
            description=self._generate_field('description'),
        )

        return section

    def yields(self, attribute):
        """Create snippet string for a list of yielded results."""
        section = '\nYields\n------\n'
        template = '{type}\n\t{description}\n'

        section += template.format(
            type=self._generate_field('type', attribute['type']),
            description=self._generate_field('description'),
        )

        return section

    def raises(self, attributes):
        """Create snippet string for a list of raiased exceptions."""
        section = '\nRaises\n------\n'
        template = '{name}\n\t{description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr),
                description=self._generate_field('description'),
            )

        return section

    def variables(self, attributes):
        """Create snippet string for a list of variables."""
        section = '\nAttributes\n----------\n'
        template = '{name} : {{{type}}}\n\t{description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                type=self._generate_field('type', attr['type']),
                description=self._generate_field('description'),
            )

        return section
