"""Default Formatter for DocBlock."""
from .base import Base


class DocblockFormatter(Base):
    """Documentation Formatter Class."""

    name = 'docblock'

    def decorators(self, attributes):
        """Create snippet string for a list of decorators."""
        section = '\nDecorators:\n'
        template = '\t{}\n'

        for attr in attributes:
            section += template.format(attr)

        return section

    def extends(self, attributes):
        """Create snippet string for a list of extended objects."""
        section = '\nExtends:\n'
        template = '\t{}\n'

        for attr in attributes:
            section += template.format(attr)

        return section

    def arguments(self, attributes):
        """Create snippet string for a list of arguments."""
        section = '\nArguments:\n'
        template = '\t{name} {{{type}}} -- {description}\n'

        for attr in attributes['arguments']:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                type=self._generate_field('type', attr['type']),
                description=self._generate_field('description'),
            )

        if len(attributes['arguments']) == 0:
            section = ''

        section += self.keyword_arguments(attributes['keyword_arguments'])

        return section

    def keyword_arguments(self, attributes):
        """Create snippet string for a list of keyword arguments."""
        section = '\nKeyword Arguments:\n'
        template = '\t{name} {{{type}}} -- {description} (default: {{{default}}})\n'

        if len(attributes) == 0:
            return ''

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                type=self._generate_field('type', attr['type']),
                description=self._generate_field('description'),
                default=self._generate_field('default', attr['default']),
            )

        return section

    def returns(self, attribute):
        """Create snippet string for a list of return values."""
        section = '\nReturns:\n'
        template = '\t{type} -- {description}\n'

        section += template.format(
            type=self._generate_field('type', attribute['type']),
            description=self._generate_field('description'),
        )

        return section

    def yields(self, attribute):
        """Create snippet string for a list of yielded results."""
        section = '\nYields:\n'
        template = '\t{type} -- {description}\n'

        section += template.format(
            type=self._generate_field('type', attribute['type']),
            description=self._generate_field('description'),
        )

        return section

    def raises(self, attributes):
        """Create snippet string for a list of raiased exceptions."""
        section = '\nRaises:\n'
        template = '\t{name} -- {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr),
                description=self._generate_field('description'),
            )

        return section

    def variables(self, attributes):
        """Create snippet string for a list of variables."""
        section = '\nVariables:\n'
        template = '\t{name} {{{type}}} -- {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                type=self._generate_field('type', attr['type']),
                description=self._generate_field('description'),
            )

        return section
