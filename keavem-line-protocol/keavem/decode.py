from datetime import datetime
from typing import List, Union

from keavem.exceptions import DecodingUndefinedItemCount
from keavem.structure import (MeasData, MeasFileHeader, MeasInfo, MeasValue,
                              NEId)
from x690.types import GraphicString, Sequence, Type, decode
from x690.util import TypeClass, TypeNature


class ByteCodec(Type[bytes]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        return data[slc]


class StrByteCodec(Type[Union[bytes, int]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[bytes, int]:
        item = data[slc]
        if len(item) == 2:
            granularity_period = item
            # Split bytes, shift first byte, merge with second byte
            split_bytes = [
                granularity_period[i : i + 1]
                for i in range(0, len(granularity_period), 1)
            ]
            return int.from_bytes(split_bytes[0], "big") << 8 | int.from_bytes(
                split_bytes[1], "big"
            )
        return item


class StrCP2Codec(Type[Union[str, bytes, datetime]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[str, bytes, datetime]:
        chunk = data[slc]
        if isinstance(chunk, bytes) and len(chunk) == 0:
            return "1"
        if 18 >= len(chunk) > 14:
            return datetime.strptime(chunk.decode("ascii"), "%Y%m%d%H%M%S%f%z")
        return chunk


class StrCP3Codec(Type[str]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        item = data[slc]
        return item.decode("ascii")


class StrMetaCP4Codec(Type[Union[str, datetime]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 4

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[str, datetime]:
        chunk = data[slc].decode("ascii")
        if 18 >= len(chunk) > 14:
            return datetime.strptime(chunk, "%Y%m%d%H%M%S%f%z")
        return chunk


class SeqCodec(Type[Union[MeasFileHeader, NEId]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[MeasFileHeader, NEId]:
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
                file_format_version_wrapped.value,
                sender_name_wrapped.value,
                sender_type_wrapped.value,
                vendor_name_wrapped.value,
                collection_begin_time_wrapped.value,
            )
        if len(items) == 2:
            (ne_user_name_wrapped, ne_distinguished_name_wrapped) = items
            return NEId(ne_user_name_wrapped.value, ne_distinguished_name_wrapped.value)
        raise DecodingUndefinedItemCount(f"{len(items)}")


class SeqListBytesCodec(Type[Union[List[bytes], MeasInfo, MeasData]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[List[bytes], MeasInfo, MeasData]:
        chunk = data[slc]
        try:
            items, next = decode(data, slc.start, enforce_type=Sequence)
            if len(items) == 4 and isinstance(items[0], ByteCodec):
                items = []
                next_tlv = 0
                while next_tlv < len(chunk):
                    item, next_tlv = decode(chunk, next_tlv)
                    (
                        meas_start_time_wrapped,
                        granularity_period_wrapped,
                        meas_types_wrapped,
                        meas_values_wrapped,
                    ) = item
                    # meas_start_time_wrapped_decoded = datetime.strptime(meas_start_time_wrapped.value, "%Y%m%d%H%M%S%z")
                    # print(meas_start_time_wrapped_decoded)
                    items.append(
                        MeasInfo(
                            meas_start_time_wrapped.value,
                            granularity_period_wrapped.value,
                            meas_types_wrapped.value,
                            meas_values_wrapped.value,
                        )
                    )
                return items
            if len(items) == 2:
                ne_id_wrapped, meas_info_wrapped = items
                return MeasData(ne_id_wrapped.value, meas_info_wrapped.value)
            raise DecodingUndefinedItemCount(
                f"Caught undefined amout of items:{len(items)} with unkown type at items[0]: {type(items[0])}"
            )
        except:
            item, next = decode(chunk, 0)
            result = [item.pythonize()]
            while next < len(chunk):
                item, next = decode(
                    chunk,
                    next,
                )
                result.append(item.pythonize())
            return result


class ListStrCodec(Type[List[str]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> List[str]:
        chunk = data[slc]
        measure_type, next = decode(chunk, 0, enforce_type=GraphicString)
        types_wrapped = [measure_type.pythonize()]
        while next < len(chunk):
            block, next = decode(chunk, next, enforce_type=GraphicString)
            types_wrapped.append(block.pythonize())
        return types_wrapped


class ListSeqCodec(Type[List[MeasValue]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> List[MeasValue]:
        chunk = data[slc]
        items = []
        next_tlv = 0
        while next_tlv < len(chunk):
            item, next_tlv = decode(chunk, next_tlv)
            (
                obj_inst_id_wrapped,
                meas_results_wrapped,
                suspect_flag_wrapped,
            ) = item
            meas_results_decoded = [
                int.from_bytes(result, "big") for result in meas_results_wrapped.value
            ]
            items.append(
                MeasValue(
                    obj_inst_id_wrapped.value.decode("ascii"),
                    meas_results_decoded,
                    int.from_bytes(suspect_flag_wrapped.value, "big"),
                )
            )
        return items
