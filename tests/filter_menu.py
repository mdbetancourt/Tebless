# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from random import randint
from tebless.devs import Debug
from tebless.utils import Store
from tebless.widgets import FilterMenu, Window

def main():
    store = Store()
    with Window(store=store) as win:
        win += FilterMenu({
            'label': 'Filtrar: ',
            'validation': r'\d'
        }, {
            'cordy': 1,
            'items': [f'Valor {randint(0,1000):04d}' for x in range(10000)],
            'header': 'Lista',
            'footer': '{page}/{last}, Total: {count}'
        })

if __name__ == '__main__':
    with Debug(__file__):
        main()
