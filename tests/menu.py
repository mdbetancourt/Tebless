# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.widgets import Menu, Window
from tebless.themes.menu import dered

GLOBAl_STORE = {}

@Window.decorator(store=GLOBAl_STORE)
def view_menu(window):
    theme = dered(window, {
        'items': [f'Valor {x}' for x in range(100)],
    })

    window.add(Menu, **theme)

@Window.decorator(store=GLOBAl_STORE)
def view_single_menu(window):
    window.add(Menu, **{
        'items': [f'Valor {x}' for x in range(100)],
        'limit': 8,
        'header': 'Menu',
        'footer': 'Pagina {page} de {last}'
    })

def main():
    view_menu()
    view_single_menu()

if __name__ == '__main__':
    main()