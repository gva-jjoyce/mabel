import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from mabel.operators import ProfileDataOperator
from mabel.data.validator import Schema
from rich import traceback

traceback.install()


def test_profile_operator():
    # fmt: off
    TEST_DATA = [
        { "name": "Sirius Black", "age": 40, "dob": "1970-01-02", "gender": "male" },
        { "name": "Harry Potter", "age": 11, "dob": "1999-07-30", "gender": "male" },
        { "name": "Hermione Grainger", "age": 10, "dob": "1999-12-14", "gender": "female" },
        { "name": "Fleur Isabelle Delacour", "age": 11, "dob": "1999-02-08", "gender": "female" },
        { "name": "James Potter", "age": 40, "dob": "1971-12-30", "gender": "male" },
        { "name": "James Potter", "age": 0, "dob": "2010-12-30", "gender": "male" }
    ]
    TEST_SCHEMA = {
        "fields": [
            { "name": "age",     "type": "numeric" },
            { "name": "gender",  "type": "enum", "symbols": ["male", "female", "not the above"] },
            { "name": "dob",     "type": "date"    },
            { "name": "name",    "type": "string"  }
        ]
    }
    # fmt: on

    pdo = ProfileDataOperator(schema=Schema(TEST_SCHEMA), inner_writer=None)

    for entry in TEST_DATA:
        pdo.execute(entry, {})

    pdo.finalize({})

    assert pdo.summary["gender"]["type"] == "enum"
    assert pdo.summary["name"]["type"] == "string"

    # there are two James Potters
    assert pdo.summary["name"]["min_length"] == 12
    assert pdo.summary["name"]["max_length"] == 23
    assert pdo.summary["name"]["items"] == 6
    assert pdo.summary["name"]["unique_values"] == 5

    assert pdo.summary["gender"]["values"]["male"] == 4
    assert pdo.summary["gender"]["values"]["female"] == 2


def test_profile_operator_binning():

    TEST_SCHEMA = {
        "fields": [
            {"name": "number", "type": "numeric"},
            {"name": "string", "type": "string"},
        ]
    }
    schema = Schema(TEST_SCHEMA)
    pdo = ProfileDataOperator(schema=schema, inner_writer=None)

    for i in range(100000):
        entry = {"number": i, "string": str(i)}
        pdo.execute(entry, {})

    outcome = pdo.finalize({})
    print(repr(pdo))


if __name__ == "__main__":  # pragma: no cover
    test_profile_operator()
    test_profile_operator_binning()

    print("okay")
