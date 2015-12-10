from .base import BaseFormatter, FormatterMeta


class GoogleFormatter(BaseFormatter):
    __metaclass__ = FormatterMeta
    name = 'google'

    def decorators(self, attributes):
        return ''

    def extends(self, attributes):
        return ''

    def arguments(self, attributes):
        section = '\Args:\n'
        template = '\t{attribute}: ${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section

    def keyword_arguments(self, attributes):
        section = '\n'
        template = '\t{attribute}: ${{{tab_index_2}:[description]}} (default: ${{{tab_index_3}:[default]}})\n'

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
        template = '\t${{{tab_index_2}:[description]}}\n\t{{{attribute}}}:\n'
        reserved_space = next(self.tab_index)

        if attribute == {}:
            attribute = '${{{tab_index_2}}}:[example]'.format(
                tab_index_2=next(self.tab_index)
            )

        section += template.format(
            attribute=attribute,
            tab_index_1=reserved_space
        )

        return section

    def yields(self, attribute):
        section = '\nYields:\n'
        template = '\t${{{tab_index_1}:[description]}}\n\t{{{attribute}}}:\n'
        reserved_space = next(self.tab_index)

        if attribute == {}:
            attribute = '${{{tab_index_2}}}:[example]'.format(
                tab_index_2=next(self.tab_index)
            )

        section += template.format(
            attribute=attribute,
            tab_index_1=reserved_space
        )

        return section

    def raises(self, attributes):
        section = '\nRaises:\n'
        template = '\t{{{attribute}}}: ${{{tab_index_1}:[description]}}\n'

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

