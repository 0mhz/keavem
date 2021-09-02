from datetime import datetime
from typing import List, Union

from x690.types import GraphicString, Sequence, Type, decode
from x690.util import TypeClass, TypeNature

from keavem.exceptions import DecodingUndefinedItemCount
from keavem.structure import MeasData, MeasFileHeader, MeasInfo, MeasValue, NEId


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


class StrMetaCP2Codec(Type[Union[str, bytes, datetime]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[str, bytes, datetime]:
        chunk = data[slc]
        if isinstance(chunk, bytes) and len(chunk) == 0:
            return "1"
        if 18 >= len(chunk) > 14:
            return datetime.strptime(chunk.decode("ascii"), "%Y%m%d%H%M%S%z")
        return chunk


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


class HeaderCodec(Type[Union[MeasFileHeader, NEId]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[MeasFileHeader, NEId]:
        items = []
        step = slc.start
        while step < slc.stop:
            item, step = decode(data, step)
            # print(item)
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
            # test
            # (ne_user_name_wrapped, ne_distinguished_name_wrapped) = items
            ne_user_name_wrapped = items[0]
            ne_distinguished_name_wrapped = items[1]
            return NEId(
                ne_user_name_wrapped.value, ne_distinguished_name_wrapped.value
            )
        raise DecodingUndefinedItemCount(f"{len(items)}")


# class SeqListBytesCodec(Type[Union[List[bytes], MeasInfo]]): #<----- Original
#     # Semantics: used for MeasResults (List[str]) and MeasInfo (Sequence of 4 items) - and MeasData?!
#     TYPECLASS = TypeClass.CONTEXT
#     NATURE = [TypeNature.CONSTRUCTED]
#     TAG = 1

#     @staticmethod
#     def decode_raw(data: bytes, slc: slice) -> Union[List[bytes], MeasInfo]:
#         chunk = data[slc]
#         try:
#             items, next = decode(chunk, 0, enforce_type=Sequence)
#             (
#                 meas_start_time_wrapped,
#                 granularity_period_wrapped,
#                 meas_types_wrapped,
#                 meas_values_wrapped,
#             ) = items
#             return MeasInfo(
#                 meas_start_time_wrapped.value,
#                 granularity_period_wrapped.value,
#                 meas_types_wrapped.value,
#                 meas_values_wrapped.value,
#             )
#         except:

#             # This is used for MeasData too which will result in a list of a list :-(
#             # It seems that the rest of the data ("MeasInfo") is not being read

#             result, next = decode(chunk, 0)
#             meas_results_wrapped = [result.pythonize()]
#             while next < len(chunk):
#                 item, next = decode(
#                     chunk,
#                     next,
#                 )
#                 meas_results_wrapped.append(item.pythonize())

#             return meas_results_wrapped

#             # res, _ = decode(chunk)
#             # return chunk


class SeqListBytesCodec(Type[Union[List[bytes], MeasInfo, MeasData]]):
    # Semantics: used for MeasResults (List[str]) and MeasInfo (Sequence of 4 items) - and MeasData?!
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 1

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[List[bytes], MeasInfo, MeasData]:
        chunk = data[slc]
        try:
            items, next = decode(chunk, 0, enforce_type=Sequence)
            # print(f"items:{items}\n")

            if len(items) == 2:
                # failhere
                ne_id_wrapped, meas_info_wrapped = items

                print(f"\nexpected_ne_id:\n{items[0]}\n")
                print(f"\nexptected_meas_info:\n{items[1]}\n")

                # return MeasData(
                #     ne_id_wrapped.value,
                #     meas_info_wrapped.value
                # )
            # if 18 >= len(items[0].value) > 14:
            if len(items) == 4:
                (
                    meas_start_time_wrapped,
                    granularity_period_wrapped,
                    meas_types_wrapped,
                    meas_values_wrapped,
                ) = items
                # failhere1
                return MeasInfo(
                    meas_start_time_wrapped.value,
                    granularity_period_wrapped.value,
                    meas_types_wrapped.value,
                    meas_values_wrapped.value,
                )
            raise DecodingUndefinedItemCount(f"{len(items)}")

        except:
            dirtydebugswitch = 1
            if dirtydebugswitch == 0:
                item, next = decode(chunk, 0)
                result = [item.pythonize()]
                while next < len(chunk):
                    item, next = decode(
                        chunk,
                        next,
                    )
                    result.append(item.pythonize())
                return result
            else:
                items = []
                next_tlv = 0
                while next_tlv < len(chunk):
                    item, next_tlv = decode(chunk, next_tlv)
                    items.append(item)
                return items


class ListStrCodec(Type[List[str]]):
    # Semantics: only used for "Measure types"
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


class ListBytesCodec(Type[MeasValue]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> MeasValue:
        sequence, _ = decode(data, slc.start)
        (
            obj_inst_id_wrapped,
            meas_results_wrapped,
            suspect_flag_wrapped,
        ) = sequence
        return MeasValue(
            obj_inst_id_wrapped.value,
            meas_results_wrapped.value,
            suspect_flag_wrapped.value,
        )
