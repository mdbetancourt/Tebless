# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
core.py

Created by Michel Betancourt on 2017.
Copyright (c) 2017 ACT. All rights reserved.
"""
__all__ = ['Window']


import blessed
from axel import Event
from tebless.devs import Widget
from tebless.utils import Store
from tebless.utils.term import echo
from tebless.utils.constants import ENTER, ESC, DOWN, UP

class Window(Widget):
    """Class that encapsulates a whole window and allows to own the elements inside.

    Usage:
        With Window (store) as window:
            Window += element
    Or:
        With Window (store) as window:
            Window.add(element, properties)
    Params:
        store - Global storage is necessary
        parent - If you do not provider it is the main window

    """
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self._width, self._height = self._term.width, self._term.height
        if not isinstance(self.store, Store):
            raise TypeError("Store is invalid")
        self._listen = True
        self._widgets = []

        self.on_enter = Event(self)
        self.on_key_arrow = Event(self)
        self.on_exit = Event(self)
        self.on_exit += self.close
        self.on_key = Event(self)

    def _paint(self):
        echo(self._term.clear)
        for widget in self._widgets:
            widget.paint()


    def close(self, *args, **kwargs):
        self._listen = False

    def listen(self):
        """Blocking call on widgets.

        """
        while self._listen:
            key = u''
            key = self._term.inkey(timeout=0.2)
            try:
                if key.code == ENTER:
                    self.on_enter(key=key)
                elif key.code in (DOWN, UP):
                    self.on_key_arrow(key=key)
                elif key.code == ESC or key == chr(3):
                    self.on_exit(key=key)
                elif key != '':
                    self.on_key(key=key)
            except KeyboardInterrupt:
                self.on_exit(key=key)

    def add(self, widget, *args, **kwargs):
        """Insert new element.

        Usage:
            window.add(widget, **{
                'prop1': val,
                'prop2': val2
            })

        """
        ins_widget = widget(*args, **kwargs)
        self.__add__(ins_widget)
        return ins_widget

    def __add__(self, widget):
        """Insert new element.

        Usage:
            window += widget(**{
                'prop1': val,
                'prop2': val2
            })

        """
        assert isinstance(widget, Widget)

        if hasattr(widget, 'ref'):
            name = widget.ref
            if name in self.store:
                raise KeyError(f'{name} key already exist')
            widget.parent = self
            self.store += {
                name: widget
            }
        widget.store = self.store

        #FIXME: Solve if after add element, add a listenner fail
        if widget.on_enter.count() > 0:
            self.on_enter += widget.on_enter
        if widget.on_key_arrow.count() > 0:
            self.on_key_arrow += widget.on_key_arrow
        if widget.on_exit.count() > 0:
            self.on_exit += widget.on_exit
        if widget.on_key.count() > 0:
            self.on_key += widget.on_key

        self._widgets.append(widget)
        return self

    @staticmethod
    def decorator(function=None, **d_wargs):
        def _decorator(func):
            def wrapper(*args, **kwargs):
                min_x = d_wargs.get('min_x', 0)
                min_y = d_wargs.get('min_y', 0)
                if blessed.Terminal().height < min_y:
                    raise RuntimeError("Window height is insufficient")
                elif blessed.Terminal().width < min_x:
                    raise RuntimeError("Window width is insufficient")
                with Window(*args, **kwargs) as win:
                    func(win, *args, **kwargs)

            return wrapper
        if function:
            return _decorator(function)
        return _decorator

    @property
    def size(self):
        """ Height and Width of window. """
        return self._width, self._height
    
    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        if not self._widgets:
            raise IndexError('Not widgets found')
        if self._parent is None:
            with self._term.cbreak(), self._term.hidden_cursor():
                self.paint()
                self.listen()
        else:
            self.paint()
            self.listen()

        if self._parent is not None:
            self._parent.paint()
