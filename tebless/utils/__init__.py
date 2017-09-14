# Copyright (c) 2017 Michel Betancourt
# 
# A part of code used of https://github.com/drgrib/dotmap
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from collections import OrderedDict, MutableMapping
from pprint import pprint
from inspect import ismethod

def dict_diff(first, second):
    """ Return a dict of keys that differ with another config object.  If a value is
        not found in one fo the configs, it will be represented by KEYNOTFOUND.
        @param first:   Fist dictionary to diff.
        @param second:  Second dicationary to diff.
        @return diff:   Dict of Key => (first.val, second.val)
    """
    diff = {}
    # Check all keys in first dict
    for key in first:
        if key not in second:
            diff[key] = (first[key], None)
        elif (first[key] != second[key]):
            diff[key] = (first[key], second[key])
    # Check all keys in second dict to find missing
    for key in second:
        if key not in first:
            diff[key] = (None, second[key])
    return diff


class Store(MutableMapping, OrderedDict):
    def __init__(self, *args, **kwargs):
        self._map = OrderedDict()
        self._dynamic = True
        if kwargs:
            if '_dynamic' in kwargs:
                self._dynamic = kwargs['_dynamic']
        if args:
            d = args[0]
            if isinstance(d, dict):
                for k,v in self.__call_items(d):
                    if isinstance(v, dict):
                        v = Store(v, _dynamic=self._dynamic)
                    if type(v) is list:
                        l = []
                        for i in v:
                            n = i
                            if type(i) is dict:
                                n = Store(i, _dynamic=self._dynamic)
                            l.append(n)
                        v = l
                    self._map[k] = v
        if kwargs:
            for k,v in self.__call_items(kwargs):
                if k is not '_dynamic':
                    self._map[k] = v

    def __call_items(self, obj):
        if hasattr(obj, 'iteritems') and ismethod(getattr(obj, 'iteritems')):
            return obj.iteritems()
        else:
            return obj.items()

    def items(self):
        return self.__call_items(self._map)

    def __iter__(self):
        return self._map.__iter__()

    def next(self):
        return self._map.next()

    def __setitem__(self, k, v):
        self._map[k] = v
    def __getitem__(self, k):
        if k not in self._map and self._dynamic and k != '_ipython_canary_method_should_not_exist_':
            # automatically extend to new Store
            self[k] = Store()
        return self._map[k]

    def __setattr__(self, k, v):
        if k in {'_map', '_dynamic', '_ipython_canary_method_should_not_exist_'}:
            super(Store, self).__setattr__(k,v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k == {'_map', '_dynamic','_ipython_canary_method_should_not_exist_'}:
            super(Store, self).__getattr__(k)
        else:
            return self[k]

    def __delattr__(self, key):
        return self._map.__delitem__(key)

    def __contains__(self, k):
        return self._map.__contains__(k)

    def __str__(self):
        items = []
        for k,v in self.__call_items(self._map):
            # bizarre recursive assignment situation (why someone would do this is beyond me)
            if id(v) == id(self):
                items.append('{0}=Store(...)'.format(k))
            else:
                items.append('{0}={1}'.format(k, repr(v)))
        joined = ', '.join(items)
        out = '{0}({1})'.format(self.__class__.__name__, joined)
        return out

    def __repr__(self):
        return str(self)


    def empty(self):
        return (not any(self))

    # proper dict subclassing
    def values(self):
        return self._map.values()

    # ipython support
    def __dir__(self):
        return self.keys()

    @classmethod
    def parseOther(self, other):
        if type(other) is Store:
            return other._map
        else:
            return other
    def __cmp__(self, other):
        other = Store.parseOther(other)
        return self._map.__cmp__(other)
    def __eq__(self, other):
        other = Store.parseOther(other)
        if not isinstance(other, dict):
            return False
        return self._map.__eq__(other)
    def __ge__(self, other):
        other = Store.parseOther(other)
        return self._map.__ge__(other)
    def __gt__(self, other):
        other = Store.parseOther(other)
        return self._map.__gt__(other)
    def __le__(self, other):
        other = Store.parseOther(other)
        return self._map.__le__(other)
    def __lt__(self, other):
        other = Store.parseOther(other)
        return self._map.__lt__(other)
    def __ne__(self, other):
        other = Store.parseOther(other)
        return self._map.__ne__(other)

    def __delitem__(self, key):
        return self._map.__delitem__(key)
    def __len__(self):
        return self._map.__len__()
    def clear(self):
        self._map.clear()
    def copy(self):
        return Store(self)
    def __copy__(self):
        return self.copy()
    def __deepcopy__(self, memo=None):
        return self.copy()
    def get(self, key, default=None):
        return self._map.get(key, default)
    def keys(self):
        return self._map.keys()
    def pop(self, key, default=None):
        return self._map.pop(key, default)
    def popitem(self):
        return self._map.popitem()
    def setdefault(self, key, default=None):
        self._map.setdefault(key, default)
    def update(self, *args, **kwargs):
        if len(args) != 0:
            self._map.update(*args)
        self._map.update(kwargs)

    @classmethod
    def fromkeys(cls, seq, value=None):
        d = Store()
        d._map = OrderedDict.fromkeys(seq, value)
        return d
    def __getstate__(self): return self.__dict__
    def __setstate__(self, d): self.__dict__.update(d)
