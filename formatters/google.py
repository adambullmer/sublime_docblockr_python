"""Default Formatter for Google."""
from .base import Base


class GoogleFormatter(Base):
    """Documentation Formatter Class."""

    name = 'google'

    def decorators(self, attributes):
        """Create snippet string for a list of decorators."""
        return ''

    def extends(self, attributes):
        """Create snippet string for a list of extended objects."""
        return ''

    def arguments(self, attributes):
        """Create snippet string for a list of arguments."""
        section = '\nArgs:\n'
        template = '\t{name}: {description}\n'

        for attr in attributes['arguments']:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        section += self.keyword_arguments(attributes['keyword_arguments'])

        if not attributes['arguments'] and not attributes['keyword_arguments']:
            section = ''

        return section

    def keyword_arguments(self, attributes):
        """Create snippet string for a list of keyword arguments."""
        section = ''
        template = '\t{name}: {description} (default: {{{default}}})\n'

        if len(attributes) == 0:
            return ''

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
                default=self._generate_field('default', attr['default']),
            )

        return section

    def returns(self, attribute):
        """Create snippet string for a list of return values."""
        section = '\nReturns:\n'
        template = '\t{description}\n\t{type}\n'

        section += template.format(
            description=self._generate_field('description'),
            type=self._generate_field('type', attribute['type']),
        )

        return section

    def yields(self, attribute):
        """Create snippet string for a list of yielded results."""
        section = '\nYields:\n'
        template = '\t{description}\n\t{type}\n'

        section += template.format(
            description=self._generate_field('description'),
            type=self._generate_field('type', attribute['type']),
        )

        return section

    def raises(self, attributes):
        """Create snippet string for a list of raiased exceptions."""
        section = '\nRaises:\n'
        template = '\t{name}: {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr),
                description=self._generate_field('description'),
            )

        return section

    def variables(self, attributes):
        """Create snippet string for a list of variables."""
        section = '\nAttributes:\n'
        template = '\t{name}: {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        return section
