import pytest
from project import parse_duration, extract_tags, normalize_status, summarize_records

def test_parse_duration():
    assert parse_duration("45m") == 45
    assert parse_duration("1h") == 60
    assert parse_duration("1h 30m") == 90
    assert parse_duration("2h30m") == 150


def test_parse_duration_invalid():
    with pytest.raises(ValueError):
        parse_duration("abc")


def test_extract_tags():
    assert extract_tags("fixed #pytest and #oop") == ["pytest", "oop"]
    assert extract_tags("no tags") == []
    assert extract_tags("#file-io #csv") == ["file-io", "csv"]


def test_normalize_status():
    assert normalize_status(" DONE ") == "done"
    assert normalize_status("blocked") == "blocked"


def test_normalize_status_invalid():
    with pytest.raises(ValueError):
        normalize_status("finished")