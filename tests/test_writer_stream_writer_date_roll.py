import time
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from mabel.adapters.null import NullWriter
from mabel.data import StreamWriter
from rich import traceback
from freezegun import freeze_time

traceback.install()


def test_stream_rollover():

    # none of these should do anything
    w = StreamWriter(
        dataset="bucket/path/file.extension",
        inner_writer=NullWriter,
        idle_timeout_seconds=1,
    )

    with freeze_time("2012-01-14"):
        lines = w.append("It's 2012")
        lines = w.append("It's still 2012")
        assert lines == 2

    with freeze_time("2017-01-14"):
        lines = w.append("Now it's 2017")
        assert lines == 1
        lines = w.append("It's still 2017")
        assert lines == 2

    time.sleep(2)


if __name__ == "__main__":  # pragma: no cover
    test_stream_rollover()

    print("okay")
