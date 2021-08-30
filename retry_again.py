from typing import List, Union
from datetime import datetime

from x690.types import Sequence, Boolean, GraphicString, Type, decode
from x690.util import TypeClass, TypeNature
from structure import *  # temporarily to facilitate developing


class MetaCP0(Type[Union[fileFormatVersion, measStartTime, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 0

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[fileFormatVersion, measStartTime, CatchMetaError]:
        try:
            items = []
            step = slc.start
            while step < slc.stop:
                item, step = decode(data, step)
                items.append(item)
            if len(items) == 1:
                if 18 >= len(data[slc]) > 14:
                    date_string = data[slc].decode("ascii")
                    time_wrapped = datetime.strptime(
                        (date_string[0:14]), "%Y%m%d%H%M%S"
                    )
                    tzone_wrapped = date_string[14 - len(date_string) :]
                    return measStartTime(time_wrapped, tzone_wrapped)
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
                return CatchMetaError(
                    f"Caught unknown items: {items}, length={len(items)}"
                )
            return CatchMetaError(
                f"Caught unknown number of items: {len(items)}"
            )
        except:
            chunk = data[slc]
            return CatchMetaError(f"Caught unknown chunk: {chunk}")


class MetaCP1(Type[Union[senderName, nEDistinguishedName, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[senderName, nEDistinguishedName, CatchMetaError]:
        try:
            chunk = data[slc]
            if len(chunk) > 1:
                sender_name_wrapped = chunk.decode("ascii").rstrip()
                return senderName(sender_name_wrapped)
            if isinstance(chunk, bytes) and len(chunk) == 0:
                if chunk == b"":
                    return nEDistinguishedName("")
            return CatchMetaError(f"Caught unknown chunk cp1: {chunk}")
        except:
            try:
                items, _ = decode(data, slc.start, strict=True)
                return CatchMetaError(f"Caught unknown items: {items}")
            except:
                chunk = data[slc]
                return CatchMetaError(
                    f"Invalid slice for granularityPeriod: {chunk}"
                )


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
        chunk = data[slc]
        try:
            vendor_name_wrapped = chunk.decode("ascii")
            return vendorName(vendor_name_wrapped)
        except:
            return CatchMetaError(
                f"Expected ascii decodable object but got {chunk}"
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


class MetaCC0(Type[Union[MeasFileHeader, NEId, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 0

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[MeasFileHeader, NEId, CatchMetaError]:
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
            return MeasFileHeader(
                fileFormatVersion(file_format_version_wrapped.value),
                senderName(sender_name_wrapped.value.value),
                senderType(sender_type_wrapped.value.value),
                vendorName(vendor_name_wrapped.value.value),
                collection_begin_time_wrapped.value,
            )
        if len(items) == 2:
            ne_user_name_wrapped, ne_distinguished_name_wrapped = items
            return NEId(ne_user_name_wrapped, ne_distinguished_name_wrapped)
        return CatchMetaError(f"Caught unknown number of items: {len(items)}")


class MetaCC1(Type[Union[measData, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = None

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[measData, CatchMetaError]:
        try:
            sequences = []
            next_tlv = slc.start
            while next_tlv < slc.stop:
                item, next_tlv = decode(data, next_tlv, enforce_type=Sequence)
                sequences.append(item)
                print(item.pretty())
        except:
            return CatchMetaError("Something went wrong")
        # if (len(items) == 2): MeasData
        # if (len(items) == 4): measInfo

        return CatchMetaError(sequences)


class MetaCC1Legacy(Type[Union[measData, MeasInfo, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 1

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[measData, MeasInfo, CatchMetaError]:
        items, _ = decode(data, slc.start)
        if type(items) == MetaCP0:
            return CatchMetaError("This shouldnt happen")

        if type(items) == Sequence:
            if len(items) == 2:
                neid_wrapped, meas_info_wrapped = items
                return measData(
                    MeasData(neid_wrapped.value, meas_info_wrapped.value)
                )
            if len(items) == 4:
                (
                    start_time_wrapped,
                    granularity_period_wrapped,
                    types_wrapped,
                    values_wrapped,
                ) = items
                return MeasInfo(
                    start_time_wrapped.value,
                    granularity_period_wrapped.value,
                    types_wrapped.value,
                    values_wrapped.value,
                )
            return CatchMetaError(
                f"Caught unknown number of items: {len(items)}"
            )
        return CatchMetaError(f"Caught unknown type of items: {type(items)}")


class Measuretypes(Type[Union[measTypesLegacy, measTypes, List[str]]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 2

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[measTypesLegacy, measTypes, List[str]]:
        chunk = data[slc]
        measure_type, next = decode(chunk, 0, enforce_type=GraphicString)
        types_wrapped = [measure_type.pythonize()]
        while next < len(chunk):
            block, next = decode(chunk, next, enforce_type=GraphicString)
            types_wrapped.append(block.pythonize())
        return types_wrapped


class MetaCC3(Type[Union[measValues, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = None

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[measValues, CatchMetaError]:
        values, _ = decode(data, slc.start)
        print(values.pretty())
        return CatchMetaError(values)
