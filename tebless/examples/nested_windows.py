from tebless.devs import init_debug
from tebless.utils import Store
from tebless.widgets import Window, Input, Label

_store = Store()


@Window.decorator(store=_store)
def main(window):
    assert isinstance(window, Window)
    _label = Label(align='center', text="Example real world",
                   width=window.width)
    _input = Input(
        label='Introduce: ',
        cordy=3,
        on_enter=lambda sender: second_window(sender.value)
    )

    window += _label, _input


@Window.decorator(store=_store)
def second_window(window, value):
    _label = Label(align='center', text=value, width=window.width)
    _input = Input(
        label='Introduce: ',
        cordy=3,
        on_enter=lambda sender: third_window(sender.value)
    )

    window += _label, _input


@Window.decorator(store=_store)
def third_window(window, value):
    assert isinstance(window, Window)
    window += Label(align='center', text=value, width=window.width)
    window.timeout(window.close, time=3)


if __name__ == '__main__':
    init_debug()
    main()
