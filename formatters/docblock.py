from .base import BaseFormatter, FormatterMeta


class DocblockFormatter(BaseFormatter):
    __metaclass__ = FormatterMeta
    name = 'docblock'

    def decorators(self, attributes):
        section = '\nDecorators:\n'
        template = '{}'

        for attr in attributes:
            section += template.format(attr)

        return section

    def extends(self, attributes):
        section = '\nExtends:\n'
        template = '\t{}\n'

        for attr in attributes:
            section += template.format(attr)

        return section

    def arguments(self, attributes):
        section = '\nArguments:\n'
        template = '\t{attribute} {{${{{tab_index_1}:[type]}}}} -- ${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section

    def keyword_arguments(self, attributes):
        section = '\nKeyword Arguments:\n'
        template = '\t{attribute} {{${{{tab_index_1}:[type]}}}} -- ${{{tab_index_2}:[description]}} (default: ${{{tab_index_3}:[default]}})\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                default='',
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
                tab_index_3=next(self.tab_index),
            )

        return section

    def returns(self, attribute):
        section = '\nReturns:\n'
        template = '\t{{{attribute}}} -- ${{{tab_index_2}:[description]}}\n'

        if attribute == {}:
            attribute = '${{{tab_index_1}:[type]}}'.format(
                tab_index_1=next(self.tab_index)
            )

        section += template.format(
            attribute=attribute,
            tab_index_2=next(self.tab_index)
        )

        return section

    def yields(self, attribute):
        section = '\nYields:\n'
        template = '\t{{{attribute}}} -- ${{{tab_index_2}:[description]}}\n'

        if attribute == {}:
            attribute = '${{{tab_index_1}}}:[type]'.format(
                tab_index_1=next(self.tab_index)
            )

        section += template.format(
            attribute=attribute,
            tab_index_2=next(self.tab_index)
        )

        return section

    def raises(self, attributes):
        section = '\nRaises:\n'
        template = '\t{{{attribute}}} -- ${{{tab_index_1}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index)
            )

        return section

    def variables(self, attributes):
        section = '\nVaribales:\n'
        template = '\t{attribute} {{${{{tab_index_1}:[type]}}}} -- ${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section
