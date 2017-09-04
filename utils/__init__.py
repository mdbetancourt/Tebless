# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


class Store(object):
    """Object for global store."""
    def __init__(self, initial={}):
        self.__dict__.update(initial)

    def __add__(self, _dict):
        self.__dict__.update(_dict)
        return self

    def __contains__(self, item):
        return item in self.__dict__

    def __str__(self):
        return str(self.__dict__)
