# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.utils.colors import red
from tebless.devs.decorators import theme
from tebless.utils.styles import underline_ns as u
__all__ = ['single', 'double']

@theme
def single(window, config):
    cx, cy = round(config.get('cordx', 0)), round(config.get('cordy', 0))
    color = config.get('color', red)
    icon = config.get('icon', '=')
    align = config.get('align', 'left')

    move = window.term.move_x
    width = round(config.get('width', window.width))

    title = config.get('header', ' Menu ')
    back = config.get('footer', '')
    tmp_text = title

    header = title.center(width, icon)
    header = header.split(tmp_text)
    header = color(header[0]) + tmp_text + color(header[1])

    icon = color(icon)

    footer = icon * width
    l_eq = move(cx) + icon + move(cx+width-1) + icon + move(2)
    if align == 'right':
        for_s = lambda x: x.rjust(width-4)
    elif align == 'center':
        for_s = lambda x: x.center(width-4)
    else:
        for_s = lambda x: x.ljust(width-4)

    return {
        'header': header,
        'footer': footer,
        'formater': lambda text, **kw: f'  {for_s(text[:width-4])}{l_eq}',
        'selector': lambda text, **kw: f'  {u(for_s(text[:width-4]))}{l_eq}',
    }


@theme
def double(window, config):
    color = config.get('color', red)
    icon = config.get('icon', '=')

    move = window.term.move_x
    width = config.get('width', window.width)

    title = config.get('header', 'Menu'.center(width-2))
    title = title[:width-3]
    back = config.get('footer', 'Pagina: {page:03d}/{last:03d}')
    line = color(icon * (width))
    l_eq = move(0) + color(icon) + move(width-1) + color(icon) + move(2)

    wrapper = f'{line}\n{l_eq}{{}}\n{line}'

    header = wrapper.format(title)
    _footer = wrapper.format(back)

    return {
        'header': header,
        'footer':_footer,
        'formater': lambda text, **kw: f'{l_eq} {text[:width]}',
        'selector': lambda text, **kw: f'{l_eq} {u(text[:width])}',
    }
