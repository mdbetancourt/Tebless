# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.devs.decorators import theme
__all__ = ['dered']

@theme
def dered(window, config):
    from tebless.utils.term import echo
    from tebless.utils.colors import red
    from tebless.utils.styles import underline_ns as u

    move = window.term.move_x
    width = config.get('width', window.width)

    title = config.get('header', 'Menu'.center(width-2))
    title = title[:width-3]
    back = config.get('footer', 'Pagina: {page:03d}/{last:03d}')
    line = red('=' * (width))
    l_eq = move(0) + red('=') + move(width-1) + red('=') + move(2)

    wrapper = f'{line}\n{l_eq}{{}}\n{line}'

    header = wrapper.format(title)
    _footer = wrapper.format(back)

    return {
        'header': header,
        'footer':_footer,
        'formater': lambda text: f'{l_eq} {text}',
        'selector': lambda text, **kw: f'{l_eq} {u(text)}',
    }

del theme
