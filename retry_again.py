from typing import List, Union
from datetime import datetime

from x690.types import Sequence, GraphicString, Type, decode
from x690.util import TypeClass, TypeNature, decode_length, visible_octets
from structure import *  # temporarily to facilitate developing


class MetaCC0(Type[Union[MeasFileHeader, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 0

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[MeasFileHeader, CatchMetaError]:
        items = []
        step = slc.start
        while step < slc.stop:
            item, step = decode(data, step)
            items.append(item)
        return CatchMetaError(items)


class MetaCP0(Type[Union[fileFormatVersion, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 0

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[fileFormatVersion, CatchMetaError]:
        try:
            items = []
            step = slc.start
            while step < slc.stop:
                item, step = decode(data, step)
                items.append(item)
            if len(items) == 1:
                if isinstance(items[0], Boolean):
                    chunk = data[slc]
                    if len(chunk) == 1:
                        int_value = int.from_bytes(chunk, "big", signed=True)
                        if len(str(int_value)) == 1:
                            return fileFormatVersion(int_value)
                        return CatchMetaError(
                            f"Caught length(int) unequal to 1: {int_value}"
                        )
                    return CatchMetaError(
                        f"Caught chunk length unequal to 1: {chunk}"
                    )
                return CatchMetaError(f"Caught unknown items: {items}")
            return CatchMetaError(
                f"Caught unknown number of items: {len(items)}"
            )
        except:
            chunk = data[slc]
            return CatchMetaError(f"Caught unknown chunk: {chunk}")


class MetaCP1(Type[Union[senderName, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[senderName, CatchMetaError]:
        try:
            chunk = data[slc]
            sender_name_wrapped = chunk.decode("ascii").rstrip()
            return senderName(sender_name_wrapped)
        except:
            try:
                items, _ = decode(data, slc.start, strict=True)
                return CatchMetaError(f"Caught unknown items: {items}")
            except:
                return CatchMetaError(f"Invalid Slice")


class MetaCP2(
    Type[Union[senderType, suspectFlag, measFileFooter, CatchMetaError]]
):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[senderType, suspectFlag, measFileFooter, CatchMetaError]:
        try:
            items, _ = decode(data, slc.start, strict=True)
            return CatchMetaError(items)
        except:
            chunk = data[slc]
            if 18 >= len(chunk) > 14:
                date_string = chunk.decode("ascii")
                time_wrapped = datetime.strptime(
                    (date_string[0:14]), "%Y%m%d%H%M%S"
                )
                tzone_wrapped = date_string[14 - len(date_string) :]
                return measFileFooter(
                    MeasFileFooter(time_wrapped, tzone_wrapped)
                )
            if isinstance(chunk, bytes):
                if chunk == b"":
                    return senderType(SenderType("1"))
                if len(chunk) == 1:
                    suspect_flag_value = int(chunk.hex())
                    if len(str(suspect_flag_value)) == 1:
                        suspect_flag_wrapped = bool(suspect_flag_value)
                        return suspectFlag(suspect_flag_wrapped)
                return CatchMetaError(
                    f"Caught chunk of type bytes with length unequal to 1: {chunk}"
                )
            return CatchMetaError(f"Caught unknown chunk: {chunk}")


class MetaCP3(Type[Union[vendorName, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 3

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[vendorName, CatchMetaError]:
        try:
            chunk = data[slc]
            vendor_name_wrapped = chunk.decode("ascii")
            return vendorName(vendor_name_wrapped)
        except:
            return CatchMetaError(
                "Expected vendor name but got something different"
            )


class MetaCP4(Type[Union[collectionBeginTime, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 4

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[collectionBeginTime, CatchMetaError]:
        chunk = data[slc]
        if 18 >= len(chunk) > 14:
            date_string = chunk.decode("ascii")
            time_wrapped = datetime.strptime(
                (date_string[0:14]), "%Y%m%d%H%M%S"
            )
            tzone_wrapped = date_string[14 - len(date_string) :]
            return collectionBeginTime(time_wrapped, tzone_wrapped)
        return CatchMetaError(f"Caught chunk length unequal to 1: {chunk}")
