# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.devs import init_debug
from tebless.utils import Store
from tebless.themes.menu import double
from tebless.widgets import Menu, Window, Label

store = Store()

@Window.decorator(store=store)
def view_menu(window):
    theme = double(window, {
        'items': [f'Valor {x}' for x in range(100)],
    })

    window += Menu(**theme)

@Window.decorator(store=store)
def view_single_menu(window):
    def update_label(sender):
        sender.store.label.value = sender.value

    window += Menu(
        items=[f'Valor {x}' for x in range(110)],
        limit=8,
        header='Menu',
        footer='Pagina {page} de {last}',
        on_change=update_label
    )
    window += Label(ref='label', cordy=10, text='mundo')

def main():
    view_menu()
    view_single_menu()

if __name__ == '__main__':
    init_debug(__file__)
    main()
