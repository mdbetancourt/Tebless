#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from tebless import __version__, __email__, __author__

with open('README.rst') as readme_file:
    readme = readme_file.read() # pylint: disable=C0103

with open('HISTORY.rst') as history_file:
    history = history_file.read()  # pylint: disable=C0103

requirements = [  # pylint: disable=C0103
    'blessed'
]

setup_requirements = []  # pylint: disable=C0103

test_requirements = []  # pylint: disable=C0103

setup(
    name='tebless',
    version=__version__,
    description="This library is a collection of widgets that supported \
     from blessed allows to create interfaces in a simple way based on events.",
    long_description=readme + '\n\n' + history,
    author=__author__,
    author_email=__email__,
    url='https://github.com/akhail/tebless',
    packages=find_packages(include=['tebless']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='tebless',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
