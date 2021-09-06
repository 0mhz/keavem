from x690 import decode

from keavem import decode as kvdecode

filename = "tests/data/file.asn1"
with open(filename, "rb") as data:
    data = data.read()
result, _ = decode(data)
# print(result.pretty())
print(result[1].pretty())
