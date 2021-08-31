from dataclasses import dataclass
from datetime import datetime
from os import stat
from typing import Union
from x690.types import Boolean, Type, decode
from x690.util import TypeClass, TypeNature
from keavem.structure import MeasFileHeader
from keavem.exceptions import DecodingUndefinedItemCount


class IntStrCodec(Type[Union[int, str]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = None  # 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[int, str]:
        items = []
        step = slc.start
        while step < slc.stop:
            item, step = decode(data, step)
            items.append(item)
        if len(items) == 1:
            if isinstance(items[0], Boolean):
                print(data[slc])
                file_format_version_wrapped = int(data[slc].hex())
                return file_format_version_wrapped
        else:
            raise DecodingUndefinedItemCount(f"{len(items)}")
        return ""  # Suppress error?


class StrCodec(Type[str]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        sender_name_wrapped, _ = decode(data, slc.start)
        # sender_name_wrapped = data[slc]
        print(sender_name_wrapped)
        # return sender_name_wrapped.decode("ascii").rstrip()
        return sender_name_wrapped


class StrBoolDatetimeCodec(Type[Union[str, bool, datetime]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = None  # 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[str, bool, datetime]:
        item, _ = decode(data, slc.start)
        return item


class HeaderCodec(Type[MeasFileHeader]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = None  # 0

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
            print(items)
            return MeasFileHeader(
                file_format_version_wrapped.value,
                sender_name_wrapped.value,
                sender_type_wrapped.value,
                vendor_name_wrapped.value,
                collection_begin_time_wrapped.value,
            )
        raise DecodingUndefinedItemCount(f"{len(items)}")
