# file deepcode ignore ReplaceAPI: test file only
"""
Test the parameter validation on the mabel.data.reader are working
"""
import datetime
import pytest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from mabel.data import Reader
from rich import traceback
from mabel.errors import InvalidReaderConfigError

traceback.install()


def test_reader_all_good():
    failed = False

    try:
        reader = Reader(
            project="",
            select=["a", "b"],
            dataset="",
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            row_format="json",
        )
    except InvalidReaderConfigError:
        failed = True

    assert not failed


def test_reader_select_not_list():
    with pytest.raises((TypeError)):
        reader = Reader(
            project="",
            select="everything",
            dataset="",
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            row_format="json",
        )


def test_reader_where_not_callable():
    with pytest.raises((TypeError)):
        reader = Reader(
            project="",
            select=["a", "b"],
            dataset="",
            where=True,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            row_format="json",
        )


def test_format_not_known():
    with pytest.raises((TypeError)):
        reader = Reader(
            project="",
            select=["a", "b"],
            dataset="",
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            row_format="excel",
        )


if __name__ == "__main__":  # pragma: no cover
    test_reader_all_good()
    test_reader_select_not_list()
    test_reader_where_not_callable()
    test_format_not_known()
