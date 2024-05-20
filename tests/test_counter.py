"""Test counter"""

from pathlib import Path

import pytest

from gungaleonline.counter import count, read_from_file, write_to_file


@pytest.fixture(name="mock_source_file")
def fixture_mock_source_file(mock_path) -> Path: # type: ignore
    """mock source_file, this file has two words."""
    words = ["hello", " ", "words"]
    source_file = mock_path / "source.txt"
    with open(source_file, "w", encoding="utf-8") as obj:
        obj.write("".join(words))
    yield source_file


def test_read_from_file(mock_source_file):
    """Test read_from_file"""
    result = read_from_file(mock_source_file)
    assert sum(1 for _ in result) == 2


def test_write_to_file(mock_path):
    """Test write_to_file"""
    dest_file = mock_path / "dest.txt"
    write_to_file(dest_file, 100)
    with open(dest_file, "r", encoding="utf-8") as obj:
        txt = obj.read()
        assert "Total count: 100" in txt


def test_count(mocker, mock_path, mock_source_file):
    """Test count"""
    mock_read_from_file = mocker.patch(
        "gungaleonline.counter.read_from_file", return_value=list(range(10))
    )
    mock_write_to_file = mocker.patch("gungaleonline.counter.write_to_file")
    dest_file = mock_path / "dest.txt"
    count(str(mock_source_file), str(dest_file))
    mock_read_from_file.assert_called_once_with(mock_source_file)
    mock_write_to_file.assert_called_once_with(dest_file, 10)
