from tebless.devs import init_debug
from tebless.utils import Store
from tebless.widgets import Window, Input, FilterMenu, Label

_store = Store()

@Window.decorator(store=_store)
def main(window, *args, **kwargs):
    assert isinstance(window, Window)
    WIDTH, HEIGHT = window.size

    _label = Label(align='center', text="Example real world", width=WIDTH)
    _input = Input(
        label='Introduce: ',
        cordy=3,
        on_enter=lambda sender, *args, **kwargs: second_window(sender.value)
    )

    window += _label, _input

@Window.decorator(store=_store)
def second_window(window, value, *args, **kwargs):
    WIDTH, HEIGHT = window.size

    _label = Label(align='center', text="Second window", width=WIDTH)
    _input = Input(
        label='Introduce: ',
        cordy=3,
        on_enter=lambda sender, *args, **kwargs: third_window(sender.value)
    )

    window += _label, _input

@Window.decorator(store=_store)
def third_window(window, value):
    WIDTH, HEIGHT = window.size

    window += Label(align='center', text="Third window", width=WIDTH)

if __name__ == '__main__':
    init_debug()
    main()
