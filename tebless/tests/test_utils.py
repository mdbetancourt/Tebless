import pytest

from tebless.utils import Store

def test_store():
    store = Store({'first': 1, 'second': 2})

    assert store.first == 1
    assert store.second == 2

    assert 'first' in store
    assert 'third' not in store

    for st in store:
        assert st == 'first' or st == 'second'

    assert store.get('first', None) == 1
    assert store.get('third', None) is None
    for _, value in store.items():
        assert 1 <= value <= 2
    store.update({'six': 6})
    assert 'six' in store
