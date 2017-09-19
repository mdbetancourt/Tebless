# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT



from pprint import pformat
from textwrap import indent
from logging import debug, basicConfig, DEBUG

def init_debug(name=None):
    basicConfig(
        filename='debug.log',
        level=DEBUG,
        filemode='w',
        format="%(msg)s"
    )
    if name:
        debug(f'Debugging program: {name}')
    Debug.is_active = True

class Debug(object):
    is_active = False
    def __init__(self, obj):
        self._obj = obj

    @staticmethod
    def log(label, content=None):
        if content:
            msg = pformat(content, 2, 80, compact=True)
            debug(f"{label}:\n" + indent(msg, '  '))


    def __enter__(self):
        debug(f" < {self._obj} > ".center(80, "="))
        return self

    def __exit__(self, *args, **kwargs):
        debug(f" </ {self._obj} > ".center(80, "=") + '\n')
