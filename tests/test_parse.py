from datetime import datetime, timezone
from os.path import dirname, join

import pytest
from x690 import decode

import keavem.decode
import keavem.parse
import keavem.structure


def test_parse_header():
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as data:
        data = data.read()
    result, _ = decode(data)
    header = keavem.parse.parse_header(result[0].value)

    assert header.file_format_version == 1
    assert header.sender_name == "BSCGARE/G21Q1.1"
    assert header.sender_type == "1"
    assert header.vendor_name == "Ericsson"
    assert header.collection_begin_time == 1629796500000000000


def test_parse_footer():
    filename = join(dirname(__file__), "data", "footer.asn1")
    with open(filename, "rb") as data:
        data = data.read()
    footer = keavem.parse.parse_footer(decode(data)[0].value)
    assert footer == 1629797400.0


def test_parse():
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as data:
        data = data.read()
    result, _ = decode(data)
    # parsed = keavem.parse.parse(result)
    # assert result == ''
