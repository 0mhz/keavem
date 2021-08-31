from datetime import datetime
from typing import Union
from x690.types import Type, decode
from x690.util import TypeClass, TypeNature
from keavem.structure import MeasFileHeader
from keavem.exceptions import DecodingUndefinedItemCount


class ByteCodec(Type[bytes]):  # Isn't everything a byte codec here?
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        # return int.from_bytes(data[slc], "big")
        # do the correct decoding later
        return data[slc]


class StrByteCodec(Type[bytes]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        item = data[slc]
        # return item.decode("ascii").strip()
        return item


class StrMetaCP2Codec(Type[Union[str, datetime]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[str, datetime]:
        chunk = data[slc]
        if isinstance(chunk, bytes) and len(chunk) == 0:
            return "1"
        if 18 >= len(chunk) > 14:
            return datetime.strptime(chunk.decode("ascii"), "%Y%m%d%H%M%S%z")
        return chunk.decode("ascii")


class StrMetaCP3Codec(Type[str]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        item = data[slc]
        return item.decode("ascii")


class StrMetaCP4Codec(Type[Union[str, datetime]]):
    # En Timestamp ass och e String
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 4

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[str, datetime]:
        chunk = data[slc].decode("ascii")
        if 18 >= len(chunk) > 14:
            return datetime.strptime(chunk, "%Y%m%d%H%M%S%z")
        return chunk


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
            print(item)
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
