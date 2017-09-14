# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import functools
from tebless.utils.styles import red, white, underline_ns
from tebless.devs.decorators import theme
__all__ = ['single', 'double']

@theme
def single(window, config):
    """Single theme
    ===== Header =====
    = items          =
    ==================

    """
    cordx = round(config.get('cordx', 0))
    color = config.get('color', red)
    icon = config.get('icon', '=')
    align = config.get('align', 'left')
    term = window.term

    width = round(config.get('width', window.width))

    title = config.get('header', ' Menu ')
    header = term.center(title, width, icon)
    header = header.split(title)
    header = color(header[0]) + title + color(header[1])

    footer = color(icon * width)

    l_eq = term.move_x(cordx) + color(icon)
    l_eq += term.move_x(cordx+width-1) + color(icon) + term.move_x(cordx+2)

    if align == 'right':
        for_s = functools.partial(term.rjust, width=width-4) #*
    elif align == 'center':
        for_s = functools.partial(term.center, width=width-4) # -4 width "= text =" 
    elif align == 'left':
        for_s = functools.partial(term.ljust, width=width-4) #*
    else:
        raise ValueError("Only align center, left, right")

    return {
        'header': header,
        'footer': footer,
        'formater': lambda text, **kwargs: l_eq + for_s(text),
        'selector': lambda text, **kwargs: l_eq + underline_ns(for_s(text)),
    }


@theme
def double(window, config):
    """Double theme
    ==================
    =     Header     =
    ==================
    = items          =
    ==================
    = footer         =
    ==================

    """
    cordx = round(config.get('cordx', 0))
    color = config.get('color', red)
    icon = config.get('icon', '=')
    width = config.get('width', window.width)
    title = config.get('header', 'Menu'.center(width-2))
    back = config.get('footer', 'Pagina: {page:03d}/{last:03d}')
    align = config.get('align', 'left')

    term = window.term
    line = color(icon * width)

    l_eq = term.move_x(cordx) + color(icon)
    l_eq += term.move_x(cordx+width-1) + color(icon) + term.move_x(cordx+1)

    wrapper = f'{line}\n{l_eq}{{}}\n{line}'

    header = wrapper.format(title)
    footer = wrapper.format(back)

    if align == 'right':
        for_s = functools.partial(term.rjust, width=width-4) #*
    elif align == 'center':
        for_s = functools.partial(term.center, width=width-4) # -4 width "= text =" 
    elif align == 'left':
        for_s = functools.partial(term.ljust, width=width-4) #*
    else:
        raise ValueError("Only align center, left, right")
    return {
        'header': header,
        'footer':footer,
        'formater': lambda text, **kwargs: f'{l_eq} {for_s(text)}',
        'selector': lambda text, **kwargs: f'{l_eq} {underline_ns(for_s(text))}',
    }
