# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Test input.

"""
from tebless.devs import init_debug
from tebless.utils.styles import red
from tebless.widgets import Input, Window, Label


@Window.decorator
def view_input(window):
    """Window.

    """
    store = window.store

    def change_label(sender):
        """event func"""
        store.label.value = sender.value

    window += Input(
        label='Introducir: ',
        cursor=red('_'),
        left_l='< ',
        right_l=' >',
        on_enter=change_label,
        ref='input'
    )
    window += Label(
        cordx=28,
        ref='label'
    )

def main():
    """Main.

    """
    view_input()

if __name__ == '__main__':
    init_debug()
    main()
