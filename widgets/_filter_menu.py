# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# encoding: utf-8

"""
    filter_menu.py

    Created by Michel Betancourt on 2017.
    Copyright (c) 2017 ACT. All rights reserved.
"""


__all__ = ['FilterMenu']

from tebless.devs import Widget
from tebless.widgets import Input, Menu

class FilterMenu(Widget):
    def __init__(self, parent, s_input, s_menu, **kwargs):
        Widget.__init__(self, parent, **kwargs)

        self._key = kwargs.get('key', s_menu.get('key', lambda x:x))

        self._text = ''
        _s_menu = {
            'on_enter': self._on_sel
        }
        _s_input = {
            'on_change': self._on_change_input
        }

        _s_menu.update(s_menu)
        _s_input.update(s_input)


        self._input = parent.add(Input, **_s_input)
        self._menu = parent.add(Menu, **_s_menu)

        self._items = list(self._menu.items)

    def _on_change_input(self, obj_e):
        text = self._input.value.lower()
        items = self._items

        item_filter = filter(lambda x: text in self._key(x).lower(), items)
        self._menu.items = item_filter


    def _on_sel(self, _):
        self._on_select(self._input, self._menu)
        print('e')

    def paint(self):
        self._menu.paint()
        self._input.paint()

    def destroy(self):
        self._input.destroy()
        self._menu.destroy()
