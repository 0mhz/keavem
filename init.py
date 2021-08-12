from x690 import decode
from x690.types import Type
from x690.util import decode_length, visible_octets

import etypes as etypes

file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"
header = "../e_fileheader.asn1"
cmdata = "../e_corruptedmdata.asn1"


def readFile():
    data = open(file, "rb").read()
    value, nxt = decode(data)
    print(value.pretty())

    # for x in Type.all():
    #    print(x)

    while nxt < len(data):
        value, nxt = decode(data, nxt)
        print(value.pretty())


def readSingle():
    data = open(cmdata, "rb").read()
    print(visible_octets(data))
    # print(decode_length(data, 50))
    print(decode_length(data, 1))


readSingle()
readFile()
