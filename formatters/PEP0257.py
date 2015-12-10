from .base import Base


class Pep0257Formatter(Base):
    name = 'PEP0257'

    def decorators(self, attributes):
        return ''

    def extends(self, attributes):
        return ''

    def arguments(self, attributes):
        section = '\nArguments:\n'
        template = '\t{name} -- {description}\n'

        for attr in attributes['arguments']:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        if len(attributes['arguments']) == 0:
            section = ''

        section += self.keyword_arguments(attributes['keyword_arguments'])

        return section

    def keyword_arguments(self, attributes):
        section = '\nKeyword arguments:\n'
        template = '\t{name} -- {description} (default: {{{default}}})\n'

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
        return ''

    def yields(self, attribute):
        return ''

    def raises(self, attributes):
        section = '\n'
        template = 'Raises a {{{attribute}}} ${{{tab_index_1}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index)
            )

        return section

    def variables(self, attributes):
        section = '\nVariables:\n'
        template = '\t{name} -- {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        return section
