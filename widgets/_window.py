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
from tebless.devs import Widget
from tebless.utils.term import echo

class Window(Widget):
    """Class that encapsulates a whole window and allows to own the elements inside.

    Usage:
        With Window (store) as window:
            Window.add (element, properties)

    Params:
        store - Global storage is necessary
        parent - If you do not provider it is the main window

    """
    def __init__(self, parent=None, **kwargs):
        Widget.__init__(self, parent, **kwargs)
        self._width, self._height = self._term.width, self._term.height

        self._widgets = []

    def paint(self):
        """Paint all elements.
        
        """
        echo(self._term.clear)
        for widget in self._widgets:
            widget.paint()

    def listen(self):
        """Blocking call on widgets.
        
        """
        focus = 0
        listenners = [x for x in self._widgets if x.is_listenner]
        while listenners:
            self.paint()
            res = listenners[focus].listen()
            if focus + res < 0:
                break

            focus = (focus + res) % len(listenners)


    def add(self, widget, *args, **kwargs):
        """Insert new element.

        Usage:
            window.add(widget, **{
                'prop1': val,
                'prop2': val2
            })

        """
        if 'ref' in kwargs:
            name = kwargs.pop('ref')
            if name in self._store:
                raise KeyError(f'{name} key already exist')
            ins_widget = widget(self, *args, **kwargs)
            self._store[name] = ins_widget
        else:
            ins_widget = widget(self, *args, **kwargs)
        
        self._widgets.append(ins_widget)
        return ins_widget

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
                    func(win)

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
        if len(self._widgets) == 0:
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
