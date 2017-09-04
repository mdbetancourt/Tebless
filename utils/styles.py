# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Style the text.

"""
import blessed

bold = blessed.Terminal().bold
underline = blessed.Terminal().underline
center = blessed.Terminal().center
ljust = blessed.Terminal().ljust
rjust = blessed.Terminal().rjust
def underline_ns(text):
    tmp = text.strip(' ')
    return text.replace(tmp, underline(tmp))
