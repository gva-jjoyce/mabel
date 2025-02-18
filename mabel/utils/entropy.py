"""
Ar Hap

(C) 2021 Justin Joyce.

https://github.com/joocer/arhap

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import string
from typing import Any, Union


def random_string(
    length: int = 64, characters: str = string.ascii_letters + string.digits
) -> str:
    result_str = "".join(random_choice(characters) for _ in range(length))
    return result_str


def random_int() -> int:
    """
    Select a random integer (64bit)
    """
    return bytes_to_int(os.urandom(8))


def random_range(min: int, max: int) -> int:
    """
    Select a random integer between two numbers
    """
    return (random_int() % ((max + 1) - min)) + min


def bytes_to_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, "big")


def random_choice(options: Union[list, str]) -> Any:
    """
    Select an item from a list of values
    """
    r = random_range(0, len(options) - 1)
    return options[r]
