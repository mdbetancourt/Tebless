# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from blessed import Terminal
from events import Events
from tebless.utils import Store
from tebless.devs import get_events, echo

class Widget(object):
    """Widget BaseClass.

    """
    def __init__(self, cordx=0, cordy=0, width=20, height=1, **kwargs):
        logging.debug(f"Create a {self} with id {id(self)}: params: {kwargs}")
        self._cordx = round(cordx)
        self._cordy = round(cordy)
        self._width = round(width)
        self._height = round(height)
        self._parent = kwargs.get('parent', None)
        self._term = Terminal()
        if self._parent:
            self._store = self._parent.store
        else:
            self._store = kwargs.get('store', Store())
        self.ref = kwargs.get('ref', None)

        def debug(*_):
            """ changes debug """
            logging.debug(f"{self} changes values: {self.__dict__}")

        events = Events()

        self.on_change = events.on_change
        self.on_enter = events.on_enter
        self.on_key_arrow = events.on_key_arrow
        self.on_exit = events.on_exit
        self.on_key = events.on_key

        self.on_change += debug
        self.on_change += self.destroy
        self.on_change += self.paint

        events = get_events(kwargs)
        logging.debug(f"{self} events: {events}")
        for key, event in events.items():
            if key == 'on_enter':
                self.on_enter += lambda fn=event, *args, **kwargs: fn(self, *args, **kwargs)
            elif key == 'on_key_arrow':
                self.on_key_arrow += lambda fn=event, *args, **kwargs: fn(self, *args, **kwargs)
            elif key == 'on_exit':
                self.on_exit += lambda fn=event, *args, **kwargs: fn(self, *args, **kwargs)
            elif key == 'on_key':
                self.on_key += lambda fn=event, *args, **kwargs: fn(self, *args, **kwargs)
            elif key == 'on_change':
                self.on_change += lambda fn=event, *args, **kwargs: fn(self, *args, **kwargs)

    def paint(self, *_):
        """ Print widget in the window """
        pos = 'x: {self.x}, y: {self.y}, h: {self.height}, w: {self.width}'
        logging.debug(f"Painted {self} with {id(self)} {pos}")
        self._paint()

    def destroy(self, *_):
        """ Destroy widget in the window """
        pos = 'x: {self.x}, y: {self.y}, h: {self.height}, w: {self.width}'
        logging.debug(f"Destroy {self} with {id(self)} {pos}")
        self._destroy()

    def _paint(self):
        raise NotImplementedError("All child class of widget need implement _paint method")

    def _destroy(self):
        line = (' ' * self.width) + '\n'
        lines = line * self.height
        echo(self.term.move(self.y, self.x) + lines)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def term(self):
        return self._term

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, value):
        self._store = value

    @property
    def x(self):
        return self._cordx

    @property
    def y(self):
        return self._cordy

    @property
    def height(self):
        """ Height of window. """
        return self._height

    @property
    def width(self):
        """ Width of window. """
        return self._width

    def __str__(self):
        return self.__class__.__name__
