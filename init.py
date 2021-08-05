from x690 import decode
from x690.util import decode_length, visible_octets

from etypes import *

file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"
"""
    tag containts a single MeasFileFooter tag (Type 130, 0x82):
    82 0f 32 30 32 30 30 36  31 34 31 39 34 35 30 30   ..20200614194500
    5a 0a                                              Z.
    LengthInfo(length=15, offset=1)
"""


def readFile():
    data = open(file, "rb").read()
    value, nxt = decode(data)
    print(value.pretty())

    while nxt < len(data):
        value, nxt = decode(data, nxt)
        print(value.pretty())


def readTag():
    data = open(tag, "rb").read()
    print(visible_octets(data))
    print(decode_length(data, 1))
    # decoded, nxt = decode(data)
    print(decode(data))
    print(MeasFileFooter.decode_raw(data))
    print(MeasFileFooter.get_time(data))
    print(MeasFileFooter.get_timezone(data))


readTag()
