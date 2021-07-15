import sys

from x690 import decode

with open(sys.argv[1], "rb") as fptr:
    data = fptr.read()
print(decode(data))
