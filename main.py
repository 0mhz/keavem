import sys
from datetime import datetime
from typing import NamedTuple

from x690 import decode
from x690.types import Type
from x690.util import TypeClass, TypeNature, decode_length, visible_octets

# Fix the imports
# @M.A. The _init_ only contains "decode" for _all_
# How to import "all" of x690.types?


"""
Just ignore this. First time.

class EsnTimestamp(NamedTuple):
    value: str
#   timezone: str

# class EsnTimestamp(Type[GeneralizedTime(Type[datetime])]):
class EsnTimestamp(Type[EsnTimestamp]):
    TYPECLASS = TypeClass.CONTEXT
    # TYPECLASS = [TypeClass.CONTEXT]
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 0x82

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(2)) -> str:
        # return EsnTimestamp(data[slc].decode())
        return GeneralizedTime(data[slc].decode())


             types.py:119
                def decode(
                data: bytes,
                start_index: int = 0,
                enforce_type: Optional[TypeType[TPopType]] = None,
                strict: bool = False,
                ) -> Tuple[TPopType, int]:


    def encode_raw(self) -> bytes:
        return self.pyvalue._asdict().encode("utf8")

"""


class MeasFileFooter(Type[bytes]):
    TAG = 130
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(2, -1)) -> str:
        data = data[slc].decode("ascii")
        return data

    # This has been made in the middle of the night.
    # Probably decode once and return objet as a tuple(time, timezone)
    def get_time(data: bytes, slc: slice = slice(2, 16)) -> str:
        data = data[slc].decode("ascii")
        return data

    def get_timezone(data: bytes, slc: slice = slice(16, -1)) -> str:
        data = data[slc].decode("ascii")
        return data


file = "../asn_test_file.asn1"
tag = "../e_measuredtime.asn1"


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
    # decoded, nxt = decode(data)
    print(decode(data))
    print(MeasFileFooter.decode_raw(data))
    print(MeasFileFooter.get_time(data))
    print(MeasFileFooter.get_timezone(data))


# readFile()
readTag()

"""
        82 0f 32 30 32 30 30 36  31 34 31 39 34 35 30 30   ..20200614194500
        5a 0a                                              Z.
        LengthInfo(length=15, offset=1)
        (<UnknownType 130 b'20200614194500Z' context/primitive/2>, 17)
"""
