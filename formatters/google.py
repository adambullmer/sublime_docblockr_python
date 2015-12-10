from .base import Base


class GoogleFormatter(Base):
    name = 'google'

    def decorators(self, attributes):
        return ''

    def extends(self, attributes):
        return ''

    def arguments(self, attributes):
        section = '\nArgs:\n'
        template = '\t{name}: {description}\n'

        for attr in attributes['arguments']:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        section += self.keyword_arguments(attributes['keyword_arguments'])

        if len(attributes['arguments']) == 0 and len(attributes['keyword_arguments']) == 0:
            section = ''

        return section

    def keyword_arguments(self, attributes):
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
        section = '\nReturns:\n'
        template = '\t{description}\n\t{type}\n'

        section += template.format(
            description=self._generate_field('description'),
            type=self._generate_field('type', attribute['type']),
        )

        return section

    def yields(self, attribute):
        section = '\nYields:\n'
        template = '\t{description}\n\t{type}\n'

        section += template.format(
            description=self._generate_field('description'),
            type=self._generate_field('type', attribute['type']),
        )

        return section

    def raises(self, attributes):
        section = '\nRaises:\n'
        template = '\t{name}: {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr),
                description=self._generate_field('description'),
            )

        return section

    def variables(self, attributes):
        section = '\nAttributes:\n'
        template = '\t{name}: {description}\n'

        for attr in attributes:
            section += template.format(
                name=self._generate_field('name', attr['name']),
                description=self._generate_field('description'),
            )

        return section

