from .base import BaseFormatter, FormatterMeta


class Pep0257Formatter(BaseFormatter):
    __metaclass__ = FormatterMeta
    name = 'PEP0257'

    def decorators(self, attributes):
        return ''

    def extends(self, attributes):
        return ''

    def arguments(self, attributes):
        section = '\nArguments:\n'
        template = '\t{attribute} -- ${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section

    def keyword_arguments(self, attributes):
        section = '\nKeyword arguments:\n'
        template = '\t{attribute} -- ${{{tab_index_2}:[description]}} (default: ${{{tab_index_3}:[default]}})\n'

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
        section = '\nVaribales:\n'
        template = '\t{attribute} -- ${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section
