from dataclasses import dataclass
from datetime import date, datetime, time
from os import stat
from typing import List, Union

from x690.types import GraphicString, Integer, Type, decode
from x690.util import TypeClass, TypeNature, visible_octets


class Wrapper(Type[bytes]):
    TAG = 1
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        value, _ = decode(data[slc])
        print(value.pretty())
        return value


class CorpName(Type[str]):  # OctetString
    TAG = 0x04
    NATURE = [TypeNature.PRIMITIVE, TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return data[slc].decode("ascii")


class NameWrapper(Type[str]):  # OctetString
    """
    Might be corporation name or firstname/lastname of a person
    Since we can't reference the previous or next instance(s), we can
    only differ between corporation name or person name depending on
    the state of the first char- no! "some example" ruins this.
    """

    TAG = 0x04
    NATURE = [TypeNature.PRIMITIVE, TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        value = data[slc].decode("ascii")
        # Check if first char upper- or lowercase
        return value


class PersonDetailsWrapper(Type[bytes]):
    TAG = 2
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        value, _ = decode(data[slc])
        print(value.pretty())
        return value


class ImmatriculNum(Type[int]):
    # Integer
    SIGNED = True
    TAG = 0x02
    NATURE = [TypeNature.PRIMITIVE]

    @classmethod
    def decode_raw(cls, data: bytes, slc: slice = slice(None)) -> int:
        data = data[slc]
        return int.from_bytes(data, "big", signed=cls.SIGNED)


class AdditionalCorp(Type[bytes]):
    TAG = 3
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        value, _ = decode(data[slc])
        print(value.pretty())
        return value
