# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import functools

__all__ = ['Widget', 'init_debug', 'Debug', 'echo']


echo = functools.partial(print, end='', flush=True)

from ._debug import init_debug, Debug
from ._widget import Widget
