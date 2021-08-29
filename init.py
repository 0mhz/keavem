from x690 import decode
from x690.util import decode_length, visible_octets
from x690.types import Sequence, Type, decode


import retry_again as retry_again

file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"
header = "../e_fileheader.asn1"
cmdata = "../e_corruptedmdata.asn1"


def readFileInfo():
    data = open(file, "rb").read()
    document, _ = decode(data)
    print(
        f"-------------------c--------- \n{(document.pretty())}\n---------------------------- \n"
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
    while i < 3:
        print(
            f"{type(document.value[1].value[1].value[i])} contains: {type(document.value[1].value[1].value[i].value)} : Values truncated"
            # f"{type(document.value[1].value[1].value[i])} contains: {type(document.value[1].value[1].value[i].value)} : {document.value[1].value[1].value[i].value}"
            # f"{type(document.value[1].value[1].value[i])} contains: {type(document.value[1].value[1].value[i].value)}"
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
    # print(f"SenderType: {value[0].value.SenderType}")
    # print(f"FileFooter: {value[2]}")
    print(value.pretty())


def readSingle():
    data = open(cmdata, "rb").read()
    print(visible_octets(data))
    # print(decode_length(data, 50))
    print(decode_length(data, 1))


block = b"0\x81\x92aJ0H\x04\x08acmecorp0&b\x110\x0f\x04\x04John\x04\x03Doe\x02\x0209b\x110\x0f\x04\x04Jane\x04\x03Doe\x02\x0209c\x140\x12\x04\x04some\x04\x07example\x02\x01\x0caD0B\x04\x0banothercorp0,b\x140\x12\x04\x05Timon\x04\x05Baker\x02\x02\r\x05b\x140\x12\x04\x06Random\x04\x04Name\x02\x02\x11\\c\x050\x03\x02\x01\r"


def readBlock():
    data = block
    value, _ = decode(data)
    print(value.pretty())


def readTestFile():
    bscgare = "../bscgareg21q1-1.asn1"
    data = open(bscgare, "rb").read()
    result, _ = decode(data, enforce_type=Sequence)
    # print(result.pretty())
    print(f"\n\n\n{result.pretty()}\n")

    # fh = result[0]
    # print(fh)
    # ff = result[2]
    # print(ff)

    # # print("\n")

    # md = result[1]
    # print(md.pretty())

    # print(len(fh))
    # d, n = decode(fh)
    # print(type(d))
    # print(d)
    # print(n)
    # k, j = decode(fh, n)
    # print(type(k))
    # print(k)
    # a, b = decode(fh, j)
    # print(type(a))
    # print(a)
    # c, e = decode(fh, b)
    # print(type(c))
    # print(c)
    # f, g = decode(fh, e)
    # print(type(f))
    # print(f)
    # l, m = decode(fh, g)
    # print(type(l))
    # print(l)

    # mdv: collisions.MeasData = result[1].value
    # ff: collisions.MeasFileHeader = result[2].value

    # print(f"{type(md)} expecting: Data")
    # for items in md.value:
    #     #print(f"in Data: {type(items)} with type:value {type(items.value)} : {items.value}")
    # print(f"in Data: {type(items)} with type {type(items.value)}")

    # for seq in items.value:
    #    print(seq)


def demo():
    doc = open(file, "rb").read()
    print(doc[:100])
    data = b"\x81\x17BSCGARE/G18Q4/03       "
    result, _ = decode(data)
    print(result)


# demo()
readTestFile()
# readFileInfo()

# readBlock()
