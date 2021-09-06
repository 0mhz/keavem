from datetime import datetime, timezone
from os.path import dirname, join

from x690 import decode


def get_data_chunk(item_pos):
    filename = join(dirname(__file__), "data", "file.asn1")
    with open(filename, "rb") as data:
        data = data.read()
    result, _ = decode(data[item_pos:])
    print(result.pretty())
    return result
