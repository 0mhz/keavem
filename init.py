from x690 import decode
from x690.util import decode_length, visible_octets

import etypes as etypes

file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"
header = "../e_fileheader.asn1"


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

    print(etypes.FileFooter.decode_raw(data))
    print(etypes.FileFooter.use_gentime(data))


def readHeader():
    data = open(header, "rb").read()
    print(visible_octets(data))
    print(decode_length(data, 1))


# readTag()
readFile()
readHeader()
