========
Tutorial
========

In this tutorial, we'll assume that tebless is already installed on your system.
If that's not the case, see :ref:`installation` .

This tutorial will walk you through these tasks:

Basic application
=================

1. The Window widget component.
2. Creating a new basic hello world application with label widget.

Window widget
-------------

Before beginning we must understand how the library should work.
This is separated by windows which have elements inside which draws the main component is the Window widget

This has 2 ways to use it you can use the one that seems more comfortable.

The first way using the reserved word ``with``::

    from tebless.widgets import Window

    with Window() as win:
        pass

As you can see it is necessary to store the window instance in a variable,
this is necessary to use it in the future to add components.

The second way using the window decorator::

    from tebless.widgets import Window

    @Window.decorator
    def main_window(win):
        pass

    main_window()

But if you execute this right now you will get an exception ``Not widgets found``.
In the next section we can see how we use the label component next to window to show a hello world

Label widget
------------

In the previous section we saw the window component now we can combine it with this to make
our hello world. Our first step will be to create our window.::

    from tebless.widgets import Window

    @Window.decorator(main=True)
    def main_window(win):
        pass

So far we have not seen anything new only the main property that allows us to automatically
execute a window in the whole application there should only be a window with this
property if you decide to use it.::

    from tebless.widgets import Window, Label
    
    @Window.decorator(main=True)
    def main_window(window):
        window += Label(
            text='Hello world!',
        )

This works! It is our first hello world.
But it is not the best hello world that has been seen let's make it more beautiful.::

    from tebless.widgets import Window, Label
    
    @Window.decorator(main=True)
    def main_window(window):
        WIDTH, HEIGHT = window.size

        window += Label(
            cordy=HEIGHT / 2 - 1,
            text='Hello world!',
            width=WIDTH,
            align='center',
        )

Better! now we have a Label centered vertically and horizontally, window provide
a property named ``size`` that contain the ``HEIGHT`` and ``WIDTH`` of terminal window, this is too easy!.
In the next section we can see new widgets and more advance examples.

Dynamic application
===================

1. See the input widget and properties.
2. See the menu widget.
3. Create with an input and a menu widget we obtain a filtered menu.
4. Use included filter menu.
5. Shared data between widgets with store.

Input widget
------------

We have an exciting widget that allows us to capture user
data is called Input let's see how it is used.::

    from tebless.widgets import Window, Input

    @Window.decorator
    def main_window(win):
        win += Input(
            label='Your name: '
        )


    if __name__ == '__main__':
        main_window()

However, the previous example does not do anything.::

    from tebless.widgets import Window, Input, Label

    @Window.decorator(main=True)
    def view_input(window):
        label = Label(text='')

        def change_label(obj):
            label.value = f'Hello {obj.value}'

        window += Input(
            cordy=2,
            label='Your name: ',
            on_enter=change_label,
            max_len=15
        )
        window += label

Cool! if you enter your name, it greets you.
In this example we saw a couple of new things we did not add directly to window
the label in this way we can use it in the listenner function. By default the input
supports 6 characters so we had to increase the size for longer names.