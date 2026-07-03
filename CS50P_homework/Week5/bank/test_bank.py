from bank import value
import pytest

def test_base():
    assert value("What's up?") == 100.00
    assert value("hello?") == 0.0
    assert value("hi?") == 20.0


def test_space():
    assert value("  What's up?") == 100.00
    assert value("  hello?") == 0.0
    assert value("  hi?") == 20.0
