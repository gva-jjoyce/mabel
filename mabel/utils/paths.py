"""
Functions to help with handling file paths
"""
import pathlib
import datetime
from uuid import uuid4


def get_parts(path_string: str):
    if not path_string:
        raise ValueError("get_parts: path_string must have a value")

    path = pathlib.PurePosixPath(path_string)
    bucket = path.parts[0]

    if len(path.parts) == 1:
        parts = "partitions"  # type:ignore
        stem = None
        suffix = None
    elif path.suffix == "":
        parts = (
            pathlib.PurePosixPath("/".join(path.parts[1:-1])) / path.stem  # type:ignore
        )
        stem = None
        suffix = None
    else:
        parts = pathlib.PurePosixPath("/".join(path.parts[1:-1]))  # type:ignore
        stem = path.stem
        suffix = path.suffix

    return str(bucket), str(parts) + "/", stem, suffix


def build_path(path: str, date: datetime.date = None):

    if not path:
        raise ValueError("build_path: path must have a value")

    if not path[-1] in ["/"]:
        # process the path
        bucket, path_string, filename, extension = get_parts(path)
        if path_string != "/":
            path_string = bucket + "/" + path_string
    else:
        path_string = path

    return date_format(path_string, date).replace("{stem}", str(uuid4()))


def date_format(path_string: str, date: datetime.date = None):

    if not date:
        date = datetime.datetime.now()

    year = date.year
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"

    path_string = str(path_string)

    path_string = path_string.replace(
        "%datefolders", f"year_{year}/month_{month}/day_{day}"
    )
    path_string = path_string.replace("%date", f"{year}-{month}-{day}")

    path_string = path_string.replace(
        "{datefolders}", f"year_{year}/month_{month}/day_{day}"
    )
    path_string = path_string.replace("{date}", f"{year}-{month}-{day}")

    return path_string
