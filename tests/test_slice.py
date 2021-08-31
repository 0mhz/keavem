from os.path import dirname, join
import pytest
from x690 import decode
import keavem.slice


def test_slice_decode_sender_name():
    item_pos = 10
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data, item_pos)
    # print(data[item_pos-2:item_pos+5])
    # print(f"data[:256]: {data[:256]}")
    print(result.pretty())
    assert result.value == "BSCGARE/G21Q1.1"
