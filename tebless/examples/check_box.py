from tebless.widgets import Window, CheckBox, Label
from tebless.utils.styles import green
from tebless.utils.keyboard import KEY_F2, KEY_F3


@Window.decorator
def main(window):
    WIDTH, HEIGHT = window.size
    window += Label(text='CheckBox example', align='center', width=WIDTH)

    window += CheckBox(cordy=2, label=green('Element 1'))
    window += CheckBox(cordy=3, label=green('Element 2'), key=KEY_F2)
    window += CheckBox(cordy=4,
                       label=green('Element 3'),
                       key=KEY_F3,
                       check=lambda state: '(O)' if state else '( )'
                       )


if __name__ == '__main__':
    main()  # pylint: disable=E1120
