from os.path import dirname, join
from datetime import datetime, timezone
from x690 import decode


def get_data_chunk(item_pos):
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as data:
        data = data.read()
    result, _ = decode(data[item_pos:])
    print(result.pretty())
    return result


def test_decode_header_withbytes():
    header = get_data_chunk(5)
    assert header.value.file_format_version == b"\x01"
    assert header.value.sender_name == b"BSCGARE/G21Q1.1        "
    assert header.value.sender_type == "1"
    assert header.value.vendor_name == "Ericsson"
    assert header.value.collection_begin_time == datetime(
        2021, 8, 24, 9, 15, tzinfo=timezone.utc
    )


def test_decode_file_format_version_asbytes():
    assert get_data_chunk(0x07).value == b"\x01"


def test_decode_sender_name_asbytes():
    assert get_data_chunk(0x0A).value == b"BSCGARE/G21Q1.1        "


def test_decode_measure_start_time_asbytes():
    assert get_data_chunk(0x58).value == b"20210824093000Z"


def test_decode_obj_inst_id_asbytes():
    assert get_data_chunk(0x17B1).value == b"SUPERCH2.46-3"


def test_decode_suspect_flag_asbytes():
    assert get_data_chunk(0xE2).value == b"\x00"
