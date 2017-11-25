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

from time import sleep
from threading import Thread
from functools import partial

from events import Events
from tebless.utils import Store
from tebless.devs import Widget, echo
from tebless.utils.keyboard import KEY_ENTER, KEY_ESCAPE, KEY_DOWN, KEY_UP


class Window(Widget):
    """Class that encapsulates a whole window and allows to own the elements inside.

    :param store: Global storage is necessary
    :param parent: If you do not provider it is the main window
    :type store: Store
    :type parent: Window

    :example:

    >>> with Window (store) as window:
    ...     Window += element

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._width, self._height = self.term.width, self.term.height

        if not isinstance(self.store, Store):
            raise TypeError("Store is invalid")

        def worker(func, time):
            sleep(time)
            func()

        def timeout(func, *args, **kwargs):
            timeout = kwargs.pop('time', None)
            if timeout is None:
                raise TypeError("take two arguments func and time")
            thread = Thread(target=worker, args=(
                partial(func, *args, **kwargs), timeout))
            thread.start()

        self.timeout = timeout
        self._is_active = False
        self._listen = True
        self._widgets = []
        events = Events()
        self.on_enter = events.on_enter
        self.on_key_arrow = events.on_key_arrow
        self.on_exit = events.on_exit
        self.on_exit += self.close
        self.on_key = events.on_key

    def paint(self):
        echo(self.term.clear)
        for widget in self._widgets:
            widget.paint()

    def close(self):
        """Close this window.

        """
        self._listen = False

    def listen(self):
        """Blocking call on widgets.

        """
        while self._listen:
            key = u''
            key = self.term.inkey(timeout=0.2)
            try:
                if key.code == KEY_ENTER:
                    self.on_enter(key=key)
                elif key.code in (KEY_DOWN, KEY_UP):
                    self.on_key_arrow(key=key)
                elif key.code == KEY_ESCAPE or key == chr(3):
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
        self.__iadd__(ins_widget)
        return ins_widget

    def __iadd__(self, widgets):
        """Insert new element.

        Usage:
            window += widget(**{
                'prop1': val,
                'prop2': val2
            })

        """
        if not isinstance(widgets, (list, tuple)):
            if not isinstance(widgets, Widget):
                raise TypeError("Only Widgets and list of widgets")
            widgets = [widgets]

        for widget in widgets:
            if not isinstance(widget, Widget):
                raise TypeError("Only Widgets")
            if widget.ref:
                name = widget.ref
                if name in self.store:
                    raise KeyError(name + ' key already exist')
                self.store.update({
                    name: widget
                })
            widget.parent = self
            widget.store = self.store
            # FIXME: Solve if after add element, add a listenner fail
            self.on_enter += widget.on_enter
            self.on_key_arrow += widget.on_key_arrow
            self.on_exit += widget.on_exit
            self.on_key += widget.on_key

            self._widgets.append(widget)
            if self._is_active:
                widget.paint()
        return self

    @staticmethod
    def decorator(function=None, **d_wargs):
        def _decorator(func):
            def wrapper(*args, **kwargs):
                min_x = d_wargs.get('min_x', 0)
                min_y = d_wargs.get('min_y', 0)
                if 'store' in d_wargs and 'store' in kwargs:
                    raise SyntaxError("store argument repeated")
                elif 'store' in d_wargs:
                    store = d_wargs.get('store')
                elif 'store' in kwargs:
                    store = kwargs.pop('store')
                else:
                    store = Store()

                if not store.get('windows'):
                    store.windows = [None]

                tmp = None
                with Window(parent=store.windows[-1], store=store) as win:
                    tmp = win
                    store.windows.append(tmp)
                    if win.height < min_y:
                        raise RuntimeError("Window height is insufficient")
                    elif win.width < min_x:
                        raise RuntimeError("Window width is insufficient")
                    func(win, *args, **kwargs)
                store.windows.remove(tmp)
            if d_wargs.get('main', False) is True:
                wrapper()
            return wrapper
        if function:
            return _decorator(function)
        return _decorator

    @property
    def size(self):
        """ Height and Width of window. """
        return self._width, self._height

    def __enter__(self):
        echo(self.term.clear)
        return self

    def __exit__(self, _type, _value, _traceback):
        if not self._widgets:
            raise IndexError('Not widgets found')
        self._is_active = True
        if self._parent is None:
            with self.term.cbreak(), self.term.hidden_cursor():
                self.paint()
                self.listen()
        else:
            self.paint()
            self.listen()

        if self._parent is not None:
            self._parent.paint()
        else:
            echo(self.term.clear)
