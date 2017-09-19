# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
    menu.py



    Created by Michel Betancourt on 2017.
    Copyright (c) 2017 MIT. All rights reserved.
"""
from math import floor, ceil

from tebless.utils.styles import red
from tebless.devs import Widget, echo
from tebless.utils.constants import DOWN, UP

__all__ = ['Menu']

class Menu(Widget):
    """Widget show a list of elements.

    Params:
        parent - If you do not provider it is the main window
        cordx - Position on axis X
        cordy - Position on axis Y
        items - Element to show
        is_menu - Is a menu or only show items
        limit - Max items to show
        header - Text header of table
        footer - Text footer of table
        selector - A function that return text to show on select
        width - Width of table
        empty - Whats show if table is empty
        key - A function return text of object in list


    """
    def __init__(self, items=None, *args, **kwargs):
        Widget.__init__(self,
                        items=items,
                        on_key_arrow=self._on_key_arrow,
                        *args, **kwargs)

        self._items = items or []
        self._len_items = len(self._items)
        self._empty = kwargs.get('empty', ['Sin elementos'])
        self._is_menu = kwargs.get('is_menu', True)
        self._limit = round(kwargs.get('limit', 4))

        if not 'width' in kwargs:
            self._width = self.term.width

        self._header = kwargs.get('header', '')
        self._footer = kwargs.get('footer', '')

        def selector(text, **kwargs):
            return red('| ') + text if self.term.length(text) > 0 else text

        self._selector = kwargs.get('selector', selector)
        self._key = kwargs.get('key', lambda x: x)
        self._formater = kwargs.get('formater', lambda text, **kw: '  ' + text[:self._width])
        self._page = 1
        self._index = 0
        self._height = 0

    def _on_key_arrow(self, key):
        if key.code == DOWN:
            self.index = (self.index + 1) % self._len_items
        elif key.code == UP:
            self.index = (self.index - 1) % self._len_items

    def paint(self):
        self._page = ceil((self._index+1)/self._limit)

        echo(self.term.move(self.y, self.x))

        header_height, footer_height = 0, 0
        if self._header != '':
            header_height = len(self._header.split('\n'))
        if self._footer != '':
            footer_height = len(self._footer.split('\n'))

        items = self.items if self.items else self._empty
        first = floor(self._index/self._limit)*self._limit
        max_page = ceil(len(items) / self._limit)

        items = items[first:self._limit+first]

        vars_op = {
            'page': self._page,
            'last': max_page,
            'count': self._len_items
        }

        ## Print header
        if self._header != '':
            echo(self._header.format(**vars_op) + '\n')
        self._height = header_height

        ## Print elements
        for idx, item in enumerate(items):
            array_text = self._key(item)
            if isinstance(array_text, str):
                array_text = [array_text]
            for index, text in enumerate(array_text):
                echo(self.term.move_x(self.x))
                tmp = self._formater(**{
                    'text': text,
                    'index': index,
                    'lenght': len(array_text)
                })
                pos = self._index % self._limit == idx
                if pos and self._is_menu and text != '':
                    tmp = self._selector(**{
                        'text': text[:self.width],
                        'index': pos,
                        'lenght': len(array_text)
                    })
                tmp += '\n'
                self._height += tmp.count('\n')
                echo(tmp)

        ## Print footer
        if self._footer != '':
            echo(self.term.move_x(self.x))
            echo(self._footer.format(**vars_op))
        self._height += footer_height

    @property
    def value(self):
        return self.items[self._index]

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        self.on_change()

    @property
    def items(self):
        return list(self._items)

    @items.setter
    def items(self, value):
        self._index = 0
        self._items = list(value)
        self._len_items = len(self._items)
        self.on_change()
