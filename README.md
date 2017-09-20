# Tebless
[![Build Status](https://travis-ci.org/Akhail/Tebless.svg?branch=master)](https://travis-ci.org/Akhail/Tebless)
This library is a collection of widgets that supported from blessed allows to create interfaces in a simple way based on events.

## Table of contents
- [Tebless](#tebless)
    - [Table of contents](#table-of-contents)
    - [How to install](#how-to-install)
    - [Example of usage](#example-of-usage)
    - [License](#license)
    - [Authors](#authors)
## How to install

```bash
pip install tebless
```

## Example of usage
This will render a label containing the text 'Hello world!', centered horizontally and vertically.

```python
from tebless.widgets import Label, Window, Input

@Window.decorator(main=True, min_y=10)
def view(window):
    WIDTH, HEIGHT = window.size
    def callback(evt):
        evt.store.label.value = evt.value

    window += Label(
        cordy=HEIGHT / 2 - 1,
        text='Hello world!',
        width=WIDTH,
        align='center',
        ref='label'
    )
    window += Input(
        width=WIDTH,
        cordx=WIDTH / 3,
        on_enter=callback
    )

```
so easy is placed a text in the console that changes with the input and limit min height window
you can also avoid access to the store

```python
from tebless.widgets import Label, Window, Input

@Window.decorator(min_y=10)
def view(window):
    WIDTH, HEIGHT = window.size

    label = Label(
        cordy=HEIGHT / 2 - 1,
        text='Hello world!',
        width=WIDTH,
        align='center'
    )

    def callback(evt):
        label.value = evt.value

    window += label
    window += Input(
        width=WIDTH,
        cordx=WIDTH / 3,
        on_enter=callback
    )
if __name__ == "__main__":
    view()
```

## License
Tebless is MIT licensed. See the [LICENSE](LICENSE) for details.

## Authors
Please see the [AUTHORS](AUTHORS)