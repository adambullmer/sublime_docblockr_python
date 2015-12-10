from .base import BaseFormatter, FormatterMeta


class NumpyFormatter(BaseFormatter):
    __metaclass__ = FormatterMeta
    name = 'numpy'

    def decorators(self, attributes):
        return ''

    def extends(self, attributes):
        return ''

    def arguments(self, attributes):
        section = '\nParameters\n----------\n'
        template = '{attribute} : {{${{{tab_index_1}:[type]}}}}\n\t${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section

    def keyword_arguments(self, attributes):
        section = '\n'
        template = '{attribute} : {{${{{tab_index_1}:[type]}}}}, optional\n'
        template += '\t${{{tab_index_2}:[description]}} '
        template += '(the default is ${{{tab_index_3}:[default]}}, which ${{{tab_index_4}:[description]}})\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                default='',
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
                tab_index_3=next(self.tab_index),
                tab_index_4=next(self.tab_index),
            )

        return section

    def returns(self, attribute):
        section = '\nReturns\n-------\n'
        template = '{{{attribute}}}\n\t${{{tab_index_2}:[description]}}\n'

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
        section = '\nYields\n------\n'
        template = '{{{attribute}}}\n\t${{{tab_index_2}:[description]}}\n'

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
        section = '\nRaises\n------\n'
        template = '{{{attribute}}}\n\t${{{tab_index_1}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index)
            )

        return section

    def variables(self, attributes):
        section = '\nAttributes\n----------\n'
        template = '{attribute} : {{${{{tab_index_1}:[type]}}}}\n\t${{{tab_index_2}:[description]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section
