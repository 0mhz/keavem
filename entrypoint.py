from x690 import decode

from keavem import decode as kdecode

filename = "tests/data/file.asn1"
with open(filename, "rb") as data:
    data = data.read()
result, _ = decode(data)
print(result.pretty())
