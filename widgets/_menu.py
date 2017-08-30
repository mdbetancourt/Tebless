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
from tebless.devs import Widget
from tebless.utils.term import echo
from tebless.utils.colors import red

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

    Events:
        on_enter - Callback on enter

    """
    def __init__(self, parent, items=None, **kwargs):
        Widget.__init__(self, parent, **kwargs)

        self._items = items or []
        self._empty = kwargs.get('empty', ['Sin elementos'])
        self._is_menu = kwargs.get('is_menu', True)
        self._limit = kwargs.get('limit', 4)
        if not 'width' in kwargs:
            self._width = parent.width
        self._header = kwargs.get('header', '')
        self._footer = kwargs.get('footer', '')

        def selector(text, **kwargs):
            return red('| ') + text if len(text) > 0 else text

        self._selector = kwargs.get('selector', selector)
        self._key = kwargs.get('key', lambda x: x)
        self._formater = kwargs.get('formater', lambda x: '  ' + x[:self._width-2])
        self._listen = False
        self._page = 1
        self._current = 0
        self._height = 0

    def listen(self):
        if not self._is_menu or not self.items:
            return 1

        key = u''
        key = self._term.inkey(timeout=0.2)
        if key.code == self._term.KEY_ENTER:
            return self._on_enter(self) or 1
        elif key.code == self._term.KEY_DOWN:
            self._current = (self._current + 1) % len(self.items)
        elif key.code == self._term.KEY_UP:
            self._current = (self._current - 1) % len(self.items)
        elif key.code == self._term.KEY_ESCAPE:
            return -1
        return 0

    def paint(self):
        """ Paint widget in the window """
        self.destroy()
        self._page = ceil((self._current+1)/self._limit)
        term = self._term
        echo(term.move(self.y, self.x))

        header_height = len(self._header.split('\n')) - 1
        footer_height = len(self._footer.split('\n')) - 1

        items = self.items if self.items else self._empty
        first = floor(self._current/self._limit)*self._limit
        max_page = ceil(len(items) / self._limit)

        items = items[first:self._limit+first]

        vars_op = {
            'page': self._page,
            'last': max_page,
            'count': len(self.items)
        }

        ## Print header
        if self._header != '':
            echo(self._header.format(**vars_op) + '\n')
        self._height = header_height

        ## Print elements
        for idx, item in enumerate(items):
            format_text = self._key(item).split('\n')

            for text in format_text:
                echo(term.move_x(self.x))
                tmp = self._formater(text)
                pos = self._current % self._limit == idx

                if pos and self._is_menu and text != '':
                    tmp = self._selector(**{
                        'text': text,
                        'index': pos,
                        'lenght': len(format_text)
                    })

                echo(tmp + '\n')
                self._height += 1

        ## Print footer
        if self._footer != '':
            echo(term.move_x(self.x))
            echo(self._footer.format(**vars_op))
        self._height += footer_height

    @property
    def is_listenner(self):
        return self._is_menu and self.items

    @property
    def value(self):
        return self.items[self._current]

    @property
    def index(self):
        return self._current

    @property
    def items(self):
        return list(self._items)
    
    @items.setter
    def items(self, value):
        self._current = 0
        self._items = list(value)
