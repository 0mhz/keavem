from datetime import datetime, timezone
from os.path import dirname, join
from typing import List, Sequence

import pytest
from x690 import decode

import keavem.decode
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


def test_decode_sequence_MeasData():
    meas_data = get_data_chunk(0x40)
    NEId = meas_data.value[0][0]
    MeasInfo = meas_data.value[0][1]
    assert NEId.ne_user_name == b""
    assert NEId.ne_distinguished_name == b""
    assert MeasInfo.meas_start_time == b"20210824093000Z"
    assert MeasInfo.granularity_period == b"\x03\x84"
    assert MeasInfo.meas_types == [
        "FRV1UNATT",
        "FRV2UNATT",
        "FRV3UNATT",
        "HRV1UNATT",
        "HRV2UNATT",
        "HRV3UNATT",
        "FRV5UNATT",
    ]
    assert MeasInfo.meas_values.meas_obj_inst_id == b"TRAPCOM.-"
    assert MeasInfo.meas_values.meas_results == [
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
    ]
    assert MeasInfo.meas_values.suspect_flag == b"\x00"


def test_decode_neid_user_name_bytes():
    assert get_data_chunk(0x4C).value == b""


def test_decode_neid_distinguished_name_bytes():
    assert get_data_chunk(0x4E).value == b""


def test_decode_sequence_measInfo():
    pass
    # meas_info = get_data_chunk(0x50)
    # assert meas_info.value == keavem.structure.MeasInfo(
    #     datetime(2021, 8, 24, 9, 30, tzinfo=timezone.utc),
    #     b'\x03\x84',
    #     ["FRV1UNATT", "FRV2UNATT", "FRV3UNATT", "HRV1UNATT", "HRV2UNATT", "HRV3UNATT", "FRV5UNATT"],
    #     keavem.structure.MeasValue(
    #         "TRAPCOM.-",
    #         [0, 0, 0, 0, 0, 0, 0],
    #         False
    #     )
    # )


def test_decode_sequence_measInfo_individual():
    pytest.skip()
    meas_info = get_data_chunk(0x50)
    assert meas_info.value.meas_start_time == datetime(
        2021, 8, 24, 9, 30, tzinfo=timezone.utc
    )
    assert meas_info.value.granularity_period == b"\x03\x84"
    assert meas_info.value.meas_types == [
        "FRV1UNATT",
        "FRV2UNATT",
        "FRV3UNATT",
        "HRV1UNATT",
        "HRV2UNATT",
        "HRV3UNATT",
        "FRV5UNATT",
    ]
    assert meas_info.values.meas_results == [
        "TRAPCOM.-",
        [0, 0, 0, 0, 0, 0, 0],
        False,
    ]


def test_decode_sequence_measInfo_individual_bytes():
    meas_info = get_data_chunk(0x50)
    assert meas_info.value.meas_start_time == b"20210824093000Z"
    assert meas_info.value.granularity_period == b"\x03\x84"
    assert meas_info.value.meas_types == [
        "FRV1UNATT",
        "FRV2UNATT",
        "FRV3UNATT",
        "HRV1UNATT",
        "HRV2UNATT",
        "HRV3UNATT",
        "FRV5UNATT",
    ]
    assert meas_info.value.meas_values.meas_obj_inst_id == b"TRAPCOM.-"
    assert meas_info.value.meas_values.meas_results == [
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
    ]
    assert meas_info.value.meas_values.suspect_flag == b"\x00"


def test_decode_element_MeasInfo_as_bytes():
    pytest.skip()
    assert get_data_chunk(0x55) == ""
    # This should be a sequence of 4 elements but the test is obsolete since
    # measInfo_* tests for the element that the sequence is enclosed into


def test_decode_sequence_meas_values():
    pytest.skip()
    meas_values = get_data_chunk(0xBC)
    assert meas_values.value == keavem.structure.MeasValue(
        "TRAPCOM.-", [0, 0, 0, 0, 0, 0, 0], False
    )


def test_decode_sequence_meas_values_as_bytes():
    meas_values = get_data_chunk(0xBC)
    assert meas_values.value.meas_obj_inst_id == b"TRAPCOM.-"
    assert meas_values.value.meas_results == [
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
    ]
    assert meas_values.value.suspect_flag == b"\x00"


def test_decode_measure_start_time():
    pytest.skip()
    assert get_data_chunk(0x58).value == datetime(
        2021, 8, 24, 9, 30, tzinfo=timezone.utc
    )


def test_decode_granularity_period():
    assert get_data_chunk(0x69).value == b"\x03\x84"


def test_decode_type_list():
    assert get_data_chunk(0x6D).value == [
        "FRV1UNATT",
        "FRV2UNATT",
        "FRV3UNATT",
        "HRV1UNATT",
        "HRV2UNATT",
        "HRV3UNATT",
        "FRV5UNATT",
    ]


def test_decode_types_single_type():
    assert get_data_chunk(0x6F).value == "FRV1UNATT"
    # (GraphicString('FRV1UNATT'), 11)


def test_decode_obj_inst_id():
    pytest.skip()
    assert get_data_chunk(0x17B1).value == "SUPERCH2.46-3"


def test_decode_suspect_flag():
    pytest.skip()
    assert get_data_chunk(0xE2).value == 0


def test_decode_file_footer():
    assert get_data_chunk(0xF9CB2).value == datetime(
        2021, 8, 24, 9, 30, tzinfo=timezone.utc
    )


def test_decode_egal():
    assert decode(b"\x30\x05ab")
