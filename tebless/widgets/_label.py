# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Widget Label.

This module contains the Label widget
"""

__all__ = ['Label']

from functools import partial
from tebless.devs import Widget, echo

class Label(Widget):
    """Print text in window.

    Create a new widget :class:`Label`

    :param text: What to print
    :param align: Text alignment ('cente', 'left', 'right')
    :param width: Maximum width of label is ignored if wrap is False
    :param height: Maximum height of label is ignored if wrap is False
    :param wrap: The text should be limited
    :type text: str
    :type align: str
    :type width: int, float
    :type height: int, float
    :type wrap: bool

    :Example:
    >>> from tebless.widgets import Label, Window
    >>> @Window.decorator(main=True)
    ... def view(window):
    ...     window += Label(text="Hello world!", cordx=2,
    ...                     cordy=2, width=10, height=2, align='center')

    """
    def __init__(self,
                 text='Label',
                 align='left',
                 width=20,
                 height=1,
                 *args, **kwargs):
        params = dict(text=text, align=align, width=width or 20, height=height or 0)
        super().__init__(*args, **params, **kwargs)

        self._text = text
        self._prev = ''
        self._wrap = (lambda x, **kw: [x]) if width is None else self.term.wrap

        if align == 'right':
            self._align = self.term.rjust
        elif align == 'center':
            self._align = self.term.center
        elif align == 'left':
            self._align = self.term.ljust
        else:
            raise ValueError("Only align center, left, right")

    def paint(self):
        wrapped = self._wrap(self.value, width=self.width)[:self.height]
        wrapped = map(partial(self._align, width=self.width), wrapped)
        wrapped = ''.join(
            self.term.move(idx + self.y, self.x) + value
            for idx, value in enumerate(wrapped)
        )
        echo(wrapped)

    @property
    def value(self):
        return self._text

    @value.setter
    def value(self, text):
        self._prev = self._text
        self._text = text
        self.on_change()

    def destroy(self):
        wrapped_text = self._wrap(self._prev, width=self.width)[:self.height]
        lines = ''.join(
            self.term.move(idx + self.y, self.x) + ' ' * self.term.length(text)
            for idx, text in enumerate(wrapped_text)
        )
        echo(lines)

    @property
    def height(self):
        if self._height == 0:
            return len(self._wrap(self.value, width=self.width))
        return self._height
