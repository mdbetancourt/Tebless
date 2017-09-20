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
from events import Events
from tebless.devs import Widget
from tebless.widgets import Input, Menu

class FilterMenu(Widget):
    def __init__(self, s_input, s_menu, filter_items=None, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self._text = ''
        events = Events()
        self.on_select = events.on_select

        _s_menu = {
            'on_enter': self.on_select
        }
        _s_input = {
            'on_change': self._on_change_input
        }

        _s_menu.update(s_menu)
        _s_input.update(s_input)
        self._filter = filter_items
        self._input = Input(**_s_input)
        self._menu = Menu(**_s_menu)
        self._items = list(self._menu.items)

        self.on_key += self._input.on_key
        self.on_key_arrow += self._menu.on_key_arrow
        self.on_enter += self._menu.on_enter

    def _on_change_input(self, *_):
        text = self._input.value.lower()
        def filt(text, items):
            return filter(lambda item: text.lower() in item.lower(), items)
        _filter = self._filter or filt

        item_filter = _filter(text, self._items.copy())
        self._menu.items = item_filter

    def paint(self):
        self._menu.paint()
        self._input.paint()

    def destroy(self):
        self._input.destroy()
        self._menu.destroy()
