import sys

from x690 import decode

file = "../asn_test_file.asn1"

with open(file, "rb") as fptr:
    data = fptr.read()
print(decode(data))
