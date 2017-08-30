# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import blessed
from tebless.utils.term import echo

class Widget:
    def __init__(self, parent, **kwargs):
        if parent is not None:
            self._term = parent.term
        else:
            self._term = blessed.Terminal()

        self._parent = parent
        self._cordx = round(kwargs.get('cordx', 0))
        self._cordy = round(kwargs.get('cordy', 0))
        self._width = kwargs.get('width', 20)
        self._height = kwargs.get('height', 0)

        if 'store' in kwargs:
            self._store = kwargs['store']
        else:
            self._store = parent.store

        # Events
        self._on_enter = kwargs.get('on_enter', lambda *arg: 1)
        self._on_change = kwargs.get('on_change', lambda *arg: 1)
        self._on_select = kwargs.get('on_select', lambda *arg: 1)


    def paint(self):
        """ Print widget in the window """
        pass

    def destroy(self):
        """ Destroy widget in the window """
        for y in range(self.y, self.y + self.height):
            echo(self._term.move(y, self.x) + ' ' * self.width)

    @property
    def parent(self):
        return self._parent

    @property
    def term(self):
        return self._term

    @property
    def x(self):
        return self._cordx

    @property
    def y(self):
        return self._cordy

    @property
    def store(self):
        """ Global store. """
        return self._store

    @property
    def is_listenner(self):
        return hasattr(self, 'listen')

    @property
    def height(self):
        """ Height of window. """
        return self._height

    @property
    def width(self):
        """ Width of window. """
        return self._width
    @property
    def value(self):
        return self.__str__()
