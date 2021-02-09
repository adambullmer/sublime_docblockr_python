"""Default Formatter for PEP-257."""
from .base import Base


class Pep0257Formatter(Base):
    """Documentation Formatter Class."""

    name = 'PEP0257'

    def decorators(self, attributes):
        """Create snippet string for a list of decorators."""
        return ''

    def extends(self, attributes):
        """Create snippet string for a list of extended objects."""
        return ''

    def arguments(self, attributes):
        """Create snippet string for a list of arguments."""
        section = '\nArguments:\n'
        template = '\t{name} -- {description}\n'

        for attr in attributes['arguments']:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        if not attributes['arguments']:
            section = ''

        section += self.keyword_arguments(attributes['keyword_arguments'])

        return section

    def keyword_arguments(self, attributes):
        """Create snippet string for a list of keyword arguments."""
        section = '\nKeyword arguments:\n'
        template = '\t{name} -- {description} (default: {{{default}}})\n'

        if not attributes:
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
        return ''

    def yields(self, attribute):
        """Create snippet string for a list of yielded results."""
        return ''

    def raises(self, attributes):
        """Create snippet string for a list of raiased exceptions."""
        section = '\n'
        template = 'Raises a {{{attribute}}} ${{{tab_index_1}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index)
            )

        return section

    def variables(self, attributes):
        """Create snippet string for a list of variables."""
        section = '\nVariables:\n'
        template = '\t{name} -- {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        return section
