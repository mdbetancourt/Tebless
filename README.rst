=======
Tebless
=======


.. image:: https://img.shields.io/pypi/v/tebless.svg
     :target: https://pypi.python.org/pypi/tebless

.. image:: https://img.shields.io/travis/akhail/tebless.svg
     :target: https://travis-ci.org/akhail/tebless

.. image:: https://readthedocs.org/projects/tebless/badge/?version=latest
     :target: http://tebless.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Akhail/Tebless/shield.svg
     :target: https://pyup.io/repos/github/Akhail/Tebless/
     :alt: Updates


This library is a collection of widgets that supported from blessed allows to create interfaces in a simple way based on events.


* Free software: MIT license
* Documentation: https://tebless.readthedocs.io.


Table of contents
-----------------

-  `Tebless`_

   -  `Table of contents`_
   -  `How to install`_
   -  `Example of usage`_

How to install
--------------

.. code:: bash

    pip install tebless

Example of usage
----------------

This will render a label containing the text ‘Hello world!’, centered
horizontally and vertically.

.. code:: python

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

so easy is placed a text in the console that changes with the input and
limit min height window you can also avoid access to the store

.. code:: python

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

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Tebless: #tebless
.. _Table of contents: #table-of-contents
.. _How to install: #how-to-install
.. _Example of usage: #example-of-usage