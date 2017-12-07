# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import functools


from ._debug import init_debug, Debug
from ._widget import Widget

echo = functools.partial(print, end='', flush=True)

__all__ = ['Widget', 'init_debug', 'Debug']
