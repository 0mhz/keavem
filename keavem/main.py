from dataclasses import dataclass
from keavem.exceptions import NoneArgumentException
from x690.types import (
    Integer,
    OctetString,
    Sequence,
    Boolean,
    GraphicString,
    Type,
    decode,
)
from x690.util import TypeClass, TypeNature
from datetime import datetime

# def calc_sum(a, b):
# if a is None:
#     raise NoneArgumentException()
# if b is None:
#     raise NoneArgumentException()
# return a + b


@dataclass
class Person:
    age: int
    name: str


@dataclass
class MeasFileHeader:
    file_format_version: int
    sender_name: str
    sender_type: str
    vendor_name: str
    collection_begin_time: datetime


class DecodingError(Exception):
    pass


class PersonCodec(Type[Person]):
    TYPECLASS = TypeClass.PRIVATE
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 15

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Person:
        person_age_wrapped, next_tlv = decode(
            data, slc.start, enforce_type=Integer
        )
        next_tlv, _ = decode(data, next_tlv, enforce_type=OctetString)
        person_name_wrapped = next_tlv
        return Person(
            person_age_wrapped.value, person_name_wrapped.value.decode("ascii")
        )


class HeaderCodec(Type[MeasFileHeader]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> MeasFileHeader:
        items = []
        step = slc.start
        while step < slc.stop:
            item, step = decode(data, step)
            items.append(item)
        if len(items) == 5:
            (
                file_format_version_wrapped,
                sender_name_wrapped,
                sender_type_wrapped,
                vendor_name_wrapped,
                collection_begin_time_wrapped,
            ) = items
            print(file_format_version_wrapped)
            return MeasFileHeader(
                file_format_version_wrapped.value,
                sender_name_wrapped.value,
                sender_type_wrapped.value,
                vendor_name_wrapped.value,
                collection_begin_time_wrapped.value,
            )
        raise DecodingError("len different")


class FileFormatVersionCodec:
    pass
