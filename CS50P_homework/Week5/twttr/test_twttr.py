import pytest
from twttr import shorten 

def test_uppercase():
    assert shorten('Apple') == 'ppl'
    assert shorten('Egg') == 'gg'
    assert shorten('Init') == 'nt'
