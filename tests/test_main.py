from os.path import dirname, join
from datetime import datetime, timezone
import pytest
from x690 import decode

import keavem.main


def test_decode_header():
    pytest.skip()
    filename = join(dirname(__file__), "data", "header.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[5:])  # Header starts at pos 5
    # print(result.pretty())
    assert result.value.file_format_version == 1
    assert result.value.sender_name == "BSCGARE/G21Q1.1"
    assert result.value.sender_type == "1"
    assert result.value.vendor_name == "Ericsson"
    assert result.value.collection_begin_time == datetime(
        2021, 8, 24, 9, 15, tzinfo=timezone.utc
    )


def test_decode_header_as_measfileheader():
    pytest.skip()
    filename = join(dirname(__file__), "data", "header.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[5:])  # Header starts at pos 5
    # assert result.value == keavem.main.MeasFileHeader(
    #     1,
    #     "BSCGARE/G21Q1.1",
    #     "1",
    #     "Ericsson",
    #     datetime(2021, 8, 24, 9, 15, tzinfo=timezone.utc),
    # )


def test_decode_file_format_version():
    item_pos = 7
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[item_pos:])
    print(result.pretty())
    assert result.value == 1


def test_decode_sender_name():
    pytest.skip()
    item_pos = 10
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data, item_pos)
    # print(data[item_pos-2:item_pos+5])
    # print(f"data[:256]: {data[:256]}")
    print(result.pretty())
    assert result.value == "BSCGARE/G21Q1.1"


def test_decode_sender_type():
    pytest.skip()
    item_pos = 0x23
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[item_pos:])
    print(result.pretty())
    assert result.value == "1"


def test_decode_obj_inst_id():
    pytest.skip()
    item_pos = 0x17B1
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as header:
        data = header.read()
    result, _ = decode(data[item_pos:])
    print(result.pretty())
    assert result.value == "SUPERCH2.46-3"
