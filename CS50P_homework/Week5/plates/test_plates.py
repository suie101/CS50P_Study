import pytest
from plates import is_valid


def test_len():
    assert is_valid("AS3134") == 1
    assert is_valid("AS31324") == 0
    assert is_valid("A") == 0


def test_firstSecondLetter():
    assert is_valid("BS3134") == 1
    assert is_valid("1S3132") == 0
    assert is_valid("S13132") == 0

def test_lastNum():
    assert is_valid("CS3145") == 1
    assert is_valid("CS313V") == 0
    assert is_valid("CS313H") == 0

def test_common():
    assert is_valid("HY3145") == 1
    assert is_valid("HY3,145") == 0
    assert is_valid("HY3.145") == 0