# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.widgets import Input, Window
from tebless.utils.colors import red

GLOBAL_STORE = {}

@Window.decorator(store=GLOBAL_STORE)
def view_input(window):
    window.add(Input, **{
        'label': 'Introducir: ',
        'cursor': red('_'),
        'left_l': '< ',
        'right_l': ' >'
    })

def main():
    view_input()

if __name__ == '__main__':
    main()
