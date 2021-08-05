from x690 import decode
from x690.util import decode_length, visible_octets

from etypes import *

file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"
"""
    The file measuredtime.asn1 contains a single FileFooter tag (0x82):
        82 0f 32 30 32 30 30 36  31 34 31 39 34 35 30 30   ..20200614194500
        5a 0a                                              Z.
        LengthInfo(length=15, offset=1)
"""
header = "../e_fileheader.asn1"
"""
    The file fileheader.asn1 contains a FileHeader tag (0xa0) with length 0x39
    (57 bytes) which contains the tags FormatVersion, Sendername, Sendertype,
    Vendorname and CollectionStartTime.
    FormatVersion [0x80, 0x01, 0x01] equals SOH (start of heading) in the
    ASCII table which is weird since an Integer is expected

    The Sendername begins with a tag 0x81 and is 23 bytes long
    T81 L17 V[  42 53 43 47 41 52 45 2f 47
                31 38 51 34 2f 30 33 20 20
                20 20 20 20 20]
    The Sendertype tag begins with 0x82 and always equals 1 in STS (proof required) so its length can
    truncated; CLASH WITH FILEFOOTER 0x82

    The LogStartTimestamp tag begins with 0x84
    84 0f 32 30 32 30 30 36 31 34 31 39 33 30 30

    The VendorName tag begins on 0x83 (length=8)

        a0 39 80 01 01 81 17 42  53 43 47 41 52 45 2f 47   .9.....BSCGARE/G
        31 38 51 34 2f 30 33 20  20 20 20 20 20 20 82 00   18Q4/03       ..
        83 08 45 72 69 63 73 73  6f 6e 84 0f 32 30 32 30   ..Ericsson..2020
        30 36 31 34 31 39 33 30  30                        061419300
        LengthInfo(length=57, offset=1)
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
    print(decode(data))

    """
        decoded, nxt = decode(data)
        print(MeasFileFooter.decode_raw(data))
        print(MeasFileFooter.get_time(data))
        print(MeasFileFooter.get_timezone(data))
        print(FileFooter.get_time(data))
        print(FileFooter.get_timezone(data))
    """

    print(FileFooter.decode_raw(data))
    print(FileFooter.use_gentime(data))


def readHeader():
    data = open(header, "rb").read()
    print(visible_octets(data))
    print(decode_length(data, 1))
    # print(decode(data))


# readTag()
readFile()
readHeader()
