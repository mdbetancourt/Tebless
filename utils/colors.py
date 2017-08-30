# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Colors funtions for terminal.

"""
import blessed

__all__ = ['green', 'yellow', 'red']

green = blessed.Terminal().green
yellow = blessed.Terminal().yellow
red = blessed.Terminal().red
white = blessed.Terminal().white