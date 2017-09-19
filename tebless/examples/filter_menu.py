# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from random import randint
from tebless.devs import init_debug
from tebless.utils import Store
from tebless.widgets import FilterMenu, Window, Label

def main():
    store = Store()
    with Window(store=store) as win:
        win += Label(
            cordy=12,
            ref='label'
        )

        def change(sender):
            store.label.value = sender.value

        win += FilterMenu({
            'label': 'Filtrar: ',
            'validation': r'\d'
        }, {
            'cordy': 1,
            'items': [f'Valor {randint(0,1000):04d}' for x in range(10000)],
            'header': 'Lista',
            'footer': '{page}/{last}, Total: {count}',
            'on_enter': change
        })

if __name__ == '__main__':
    init_debug(__file__)
    main()
