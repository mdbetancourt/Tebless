# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Commons events.

"""

def text_window(sender, *args, **kwargs):
    sender.value[1](parent=sender.parent)
