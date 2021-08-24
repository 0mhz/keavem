from x690 import decode
from x690.types import Type
from x690.util import decode_length, visible_octets

import esntypes as etypes

file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"
header = "../e_fileheader.asn1"
cmdata = "../e_corruptedmdata.asn1"


def readFileInfo():
    data = open(file, "rb").read()
    document, _ = decode(data)
    print(
        f"---------------------------- \n{(document.pretty())}\n---------------------------- \n"
    )
    print(f"{type(document.value[0])} contains: {document.value[0].value}\n")
    print(
        f"{type(document.value[1])} contains: {type(document.value[1].value)} : {document.value[1].value}\n"
    )
    print(
        f"{type(document.value[1].value[0])} contains: {type(document.value[1].value[0].value)} : {document.value[1].value[0].value}\n"
    )
    print(
        f"{type(document.value[1].value[1])} contains: {type(document.value[1].value[1].value)} : {document.value[1].value[1]}\n"
    )

    i = 0
    while i < 4:
        print(
            # f"{type(document.value[1].value[1].value[i])} contains: {type(document.value[1].value[1].value[i].value)} : {document.value[1].value[1].value[i].value}"
            f"{type(document.value[1].value[1].value[i])} contains: {type(document.value[1].value[1].value[i].value)}"
        )
        i = i + 1

    print(
        f"\n{type(document.value[2])} contains: {type(document.value[2].value)} : {document.value[2].value}"
    )

    # for x in Type.all():
    #    print(x)
    # print(document.value[0].value.VendorName)


def readFile():
    data = open(file, "rb").read()
    value, _ = decode(data)
    print(value.pretty())


def readSingle():
    data = open(cmdata, "rb").read()
    print(visible_octets(data))
    # print(decode_length(data, 50))
    print(decode_length(data, 1))


readFileInfo()
# readFile()
