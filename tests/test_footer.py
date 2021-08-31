from os.path import dirname, join
from datetime import datetime, timezone
import pytest
from x690 import decode

import keavem.main
import keavem.structure


def get_data_chunk(item_pos):
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as data:
        data = data.read()
    result, _ = decode(data[item_pos:])
    print(result.pretty())
    return result


def test_decode_file_footer():
    assert get_data_chunk(0xF9CB2).value == datetime(
        2021, 8, 24, 9, 30, tzinfo=timezone.utc
    )
