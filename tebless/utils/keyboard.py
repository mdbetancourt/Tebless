# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Global constants

"""
import sys
import blessed

TERM = blessed.Terminal()

class Keyboard(object):
    def __getattr__(self, name):
        assert isinstance(name, str)
        if name.startswith("KEY_") and name in TERM.__dict__:
            return TERM.__dict__.get(name)

        raise AttributeError(f"type object 'Keyboard' has no attribute '{name}'")


sys.modules[__name__] = Keyboard()
