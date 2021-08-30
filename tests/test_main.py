import keavem.main
from keavem.exceptions import NoneArgumentException
from x690 import decode
import pytest
from os.path import dirname, join
from datetime import datetime, timezone

# def test_sum():
#     result = calc_sum(2, 3)
#     assert result == 5

# def test_negative_pos1_sum():
#     result = calc_sum(-1, 1)
#     assert result == 0

# def test_negative_pos2_sum():
#     result = calc_sum(1, -1)
#     assert result == 0

# def test_missing_args_pos1_sum():
#     with pytest.raises(NoneArgumentException):
#         calc_sum(None, 0)

# def test_missing_args_pos2_sum():
#     with pytest.raises(NoneArgumentException):
#         calc_sum(0, None)

# def test_missing_args_sum():
#     with pytest.raises(NoneArgumentException):
#         calc_sum(None, None)


def test_decode_sequence():
    block = b"\xef\x09\x02\x01\x08\x04\x04JOHN"
    result, _ = decode(block, strict=True)
    print(result.pretty())
    assert result.value.age == 8
    assert result.value.name == "JOHN"


def test_decode_header():
    pytest.skip()
    filename = join(dirname(__file__), "data", "header.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[5:])  # Header starts at pos 5
    print(result.pretty())
    assert result.value.file_format_version == 1
    assert result.value.sender_name == "BSCGARE/G21Q1.1"
    assert result.value.sender_type == "1"
    assert result.value.vendor_name == "Ericsson"
    assert result.value.collection_begin_time == datetime(
        2021, 8, 24, 9, 15, tzinfo=timezone.utc
    )
    assert result.value == keavem.main.MeasFileHeader(
        1,
        "BSCGARE/G21Q1.1",
        "1",
        "Ericsson",
        datetime(2021, 8, 24, 9, 15, tzinfo=timezone.utc),
    )


def test_decode_file_format_version():
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[0x17B1:])  # Header starts at pos 5
    print(result.pretty())
    assert result.value.file_format_version == 1
