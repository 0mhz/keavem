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


def test_decode_header():
    pytest.skip()
    header = get_data_chunk(5)
    assert header.value.file_format_version == 1
    assert header.value.sender_name == "BSCGARE/G21Q1.1"
    assert header.value.sender_type == "1"
    assert header.value.vendor_name == "Ericsson"
    assert header.value.collection_begin_time == datetime(
        2021, 8, 24, 9, 15, tzinfo=timezone.utc
    )


def test_decode_header_as_measfileheader():
    pytest.skip()
    header = get_data_chunk(5)
    assert header.value == keavem.structure.MeasFileHeader(
        1,
        "BSCGARE/G21Q1.1",
        "1",
        "Ericsson",
        datetime(2021, 8, 24, 9, 15, tzinfo=timezone.utc),
    )


def test_decode_file_format_version():
    pytest.skip()
    assert get_data_chunk(0x07).value == 1


def test_decode_sender_name():
    pytest.skip()
    assert get_data_chunk(0x0A).value == "BSCGARE/G21Q1.1"


def test_decode_sender_type():
    assert get_data_chunk(0x23).value == "1"


def test_decode_vendor_name():
    assert get_data_chunk(0x25).value == "Ericsson"


def test_decode_collection_begin_time():
    assert get_data_chunk(0x2F).value == datetime(
        2021, 8, 24, 9, 15, tzinfo=timezone.utc
    )


def test_decode_measure_start_time():
    pytest.skip()
    assert get_data_chunk(0x58).value == datetime(
        2021, 8, 24, 9, 30, tzinfo=timezone.utc
    )


def test_decode_granularity_period():
    assert get_data_chunk(0x69).value == b"\x03\x84"


def test_decode_types_single_type():
    pytest.skip()
    assert get_data_chunk(0x71).value == "FRV1UNATT"


def test_decode_obj_inst_id():
    pytest.skip()
    assert get_data_chunk(0x17B1).value == "SUPERCH2.46-3"


def test_decode_file_footer():
    assert get_data_chunk(0xF9CB2).value == datetime(
        2021, 8, 24, 9, 30, tzinfo=timezone.utc
    )
