# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

""" Utils functions """

__all__ = ['echo', 'apply_style']

import re
import functools

echo = functools.partial(print, end='', flush=True)
def extract_styles(text):
    return re.sub(r'(\x1b\[\d+m)|(\x1b\(B\x1b\[m)', '', text)
def cut_text(text, init=0, end=0):
    tmp = extract_styles(text)
    tmp_cut = tmp[init:end]
    return text.replace(tmp, tmp_cut)
def apply_style(item, styles):
    """ """
    return functools.reduce(lambda x, fn: fn(x), [item, *styles])
