# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.devs import Debug
from tebless.utils import Store
from tebless.utils.colors import red
from tebless.widgets import Input, Window, Label

store = Store()

@Window.decorator(store=store)
def view_input(window):
    store = window.store

    def change_label(sender, *args, **kwargs):
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
    view_input()

if __name__ == '__main__':
    with Debug(__file__):
        main()
