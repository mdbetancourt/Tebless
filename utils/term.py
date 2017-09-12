# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

""" Utils functions """

__all__ = ['echo', 'apply_style']

import re
import functools
from blessed import Terminal

echo = functools.partial(print, end='', flush=True)

strip_seqs = Terminal().strip_seqs
move = lambda x, y, text: echo(Terminal().move(x, y) + text)
clear = lambda: echo(Terminal().clear)
inkey = Terminal().inkey
cbreak = Terminal().cbreak
hidden_cursor = Terminal().hidden_cursor
height = Terminal().height
width = Terminal().width
size = width, height

def apply_style(item, styles):
    """ """
    return functools.reduce(lambda x, fn: fn(x), [item, *styles])
