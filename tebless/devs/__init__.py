# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import functools
def get_events(_dict):
    return dict(filter(lambda item: 'on_' in item[0], _dict.items()))

echo = functools.partial(print, end='', flush=True)

class Debug:
    """Context Debug config a app for debug.

    """
    def __init__(self, name):
        self.name = name
        logging.basicConfig(
            filename='debug.log',
            level=logging.DEBUG,
            format="file: %(filename)s, line: %(lineno)d, Msg: %(msg)s"
        )
    def __enter__(self):
        logging.debug(f"Init instance {self.name}")
        return self
    def __exit__(self, *args, **kwargs):
        logging.debug(f"Ended instance {self.name}\n")

from ._widget import Widget
