# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

""" Utils functions """

__all__ = ['echo', 'apply_style']

import blessed
import functools

echo = functools.partial(print, end='', flush=True)

def apply_style(item, styles):
    """ """
    return functools.reduce(lambda x, fn: fn(x), [item, *styles])


