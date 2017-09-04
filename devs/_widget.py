# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import blessed
from axel import Event
from tebless.utils import Store
from tebless.devs import get_events
from tebless.utils.term import echo

class Widget(object):
    """Widget BaseClass.

    """
    def __init__(self, cordx=0, cordy=0, width=20, height=1, **kwargs):
        logging.debug(f"Create a {self} with id {id(self)}: params: {kwargs}")
        self._term = blessed.Terminal()
        self._cordx = round(cordx)
        self._cordy = round(cordy)
        self._width = round(width)
        self._height = round(height)

        self._parent = kwargs.get('parent', None)
        self._store = kwargs.get('store', Store())
        self.ref = kwargs.get('ref', None)
        def debug(*_):
            """ changes debug """
            logging.debug(f"{self} changes values: {self.__dict__}")

        self.on_change = Event(self, threads=1)
        self.on_change += debug
        self.on_change += self.destroy
        self.on_change += self.paint
        self.on_enter = Event(self, threads=1)
        self.on_key_arrow = Event(self, threads=1)
        self.on_exit = Event(self, threads=1)
        self.on_key = Event(self, threads=1)

        events = get_events(kwargs)
        logging.debug(f"{self} events: {events}")
        for key, event in events.items():
            if (isinstance(event, Event) and event.count() > 0) or not isinstance(event, Event):
                if key == 'on_enter':
                    self.on_enter += event
                elif key == 'on_key_arrow':
                    self.on_key_arrow += event
                elif key == 'on_exit':
                    self.on_exit += event
                elif key == 'on_key':
                    self.on_key += event
                elif key == 'on_change':
                    self.on_change += event

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
        raise NotImplementedError
    def _destroy(self):
        for y_val in range(self.y, self.y + self.height):
            echo(self._term.move(y_val, self.x) + (' ' * (self.width+1)))

    @property
    def term(self):
        return self._term

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value

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
