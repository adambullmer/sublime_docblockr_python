from .base import BaseFormatter, FormatterMeta


class SphinxFormatter(BaseFormatter):
    __metaclass__ = FormatterMeta
    name = 'sphinx'

    def decorators(self, attributes):
        return ''

    def extends(self, attributes):
        return ''

    def arguments(self, attributes):
        section = '\n'
        template = ':param {attribute}: ${{{tab_index_1}:[description]}}\n'
        template += ':type {attribute}: ${{{tab_index_2}:[type]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section

    def keyword_arguments(self, attributes):
        section = ''
        template = ':param {attribute}: ${{{tab_index_1}:[description]}}, defaults to ${{{tab_index_2}:[default]}}\n'
        template += ':type {attribute}: ${{{tab_index_3}:[type]}}, optional\n'

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
        section = '\n'
        template = ':returns: ${{{tab_index_1}:[description]}}\n'
        template += ':rtype: {{{attribute}}}'
        reserved_space = next(self.tab_index)

        if attribute == {}:
            attribute = '${{{tab_index_2}:[type]}}'.format(
                tab_index_2=next(self.tab_index)
            )

        section += template.format(
            attribute=attribute,
            tab_index_1=reserved_space
        )

        return section

    def yields(self, attribute):
        template = ':returns: ${{{tab_index_1}:[description]}}\n'
        template += ':rtype: {{{attribute}}}'

        if attribute == {}:
            attribute = '${{{tab_index_2}}}:[type]'.format(
                tab_index_2=next(self.tab_index)
            )

        section += template.format(
            attribute=attribute,
            tab_index_1=next(self.tab_index)
        )

        return section

    def raises(self, attributes):
        section = '\n:raises:'
        template = ' {{{attribute}}},'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index)
            )

        return section[:-1] + '\n'

    def variables(self, attributes):
        section = '\n'
        template = ':param {attribute}: ${{{tab_index_1}:[description]}}\n'
        template += ':type {attribute}: ${{{tab_index_2}:[type]}}\n'

        for attr in attributes:
            section += template.format(
                attribute=attr,
                tab_index_1=next(self.tab_index),
                tab_index_2=next(self.tab_index),
            )

        return section
