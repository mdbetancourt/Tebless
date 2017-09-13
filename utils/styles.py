# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Colors funtions for terminal.

"""
import blessed
from tebless.utils.constants import TERM
__all__ = ['green', 'yellow', 'red', 'blue']

green = TERM.green
yellow = TERM.yellow
red = TERM.red
white = TERM.white
blue = TERM.blue
underline = TERM.underline

def underline_ns(text):
    tmp = text.strip(' ')
    return text.replace(tmp, underline(tmp))
