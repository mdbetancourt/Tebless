# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Colors funtions for terminal.

"""
import sys
import blessed

TERM = blessed.Terminal()


class Style(object):
    def __getattr__(self, name):
        formatters = blessed.formatters.split_compound(name)
        compoundables, colors = blessed.formatters.COMPOUNDABLES, blessed.formatters.COLORS
        if name in colors or all(fmt in compoundables for fmt in formatters):
            return TERM.__getattr__(name)
        else:
            raise AttributeError(
                "type object 'Style' has no attribute '{}'".format(name))

    def underline_ns(self, text):
        tmp = text.strip(' ')
        return text.replace(tmp, Style().underline(tmp))


sys.modules[__name__] = Style()
