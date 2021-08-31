from typing import List, Union
from datetime import datetime

from x690.types import Sequence, GraphicString, Type, decode
from x690.util import TypeClass, TypeNature
from structure_legacy import *  # temporarily to facilitate developing


class Meta_cc0(Type[Union[MeasFileHeader, NEId, str]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 0

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[MeasFileHeader, NEId, str]:
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
        return "len(items) != 5"


class Meta_cp2(
    Type[Union[senderType, MeasFileFooter, suspectFlag, CatchMetaError]]
):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[senderType, MeasFileFooter, suspectFlag, CatchMetaError]:
        item = data[slc]
        # Please see retry_readme
        if isinstance(item, bytes):
            if item == b"":
                return senderType(SenderType("1"))
            if len(item) == 1:
                suspect_flag_value = int(item.hex())
                if len(str(suspect_flag_value)) == 1:
                    suspect_flag_wrapped = bool(suspect_flag_value)
                    return suspectFlag(suspect_flag_wrapped)
        if len(item) >= 15:
            date_string = data[slc].decode("ascii")
            time_wrapped = datetime.strptime(
                (date_string[0:14]), "%Y%m%d%H%M%S"
            )
            tzone_wrapped = date_string[14 - len(date_string) :]
            return MeasFileFooter(time_wrapped, tzone_wrapped)
        return CatchMetaError(item)


class Meta_cp0(Type[Union[fileFormatVersion, measObjInstId, str]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 0

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[fileFormatVersion, measObjInstId, str]:
        int_value = int.from_bytes(data[slc], "big", signed=True)
        if len(str(int_value)) == 1:
            return fileFormatVersion(int_value)
        # meas_obj_inst_id_wrapped, _ = decode(data, slc.start) # NUMERICSTRING AGAINNNNN
        # meas_obj_inst_id_wrapped = data[slc].decode() # invalid start byte
        # return measObjInstId(meas_obj_inst_id_wrapped[0].value)
        return "measObjInstId (Invalid slice)"


class Sendername(Type[Union[senderName, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[senderName, CatchMetaError]:
        # item, _ = decode(data, slc.start)
        try:
            value = data[slc].decode("ascii").rstrip()
            return senderName(value)
        except:
            try:
                value, _ = decode(
                    data, slc.start
                )  # data[slc] is b'\x03\x84' at this point
            except:
                return CatchMetaError("Invalid slice")
            return CatchMetaError(value)


class Sendertype(Type[str]):
    # Meta_cp2
    pass


class VendorName(Type[vendorName]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> vendorName:
        value = data[slc].decode("ascii")
        return vendorName(value)


class Meta_cp4(Type[Union[collectionBeginTime, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 4

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[collectionBeginTime, CatchMetaError]:
        item, _ = decode(
            data, slc.start
        )  # This contains NumericString() again. I don't know what's wrong.
        date_string = data[slc].decode("ascii")
        time_wrapped = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
        tzone_wrapped = date_string[14 - len(date_string) :]
        return collectionBeginTime(time_wrapped, tzone_wrapped)


class Data(Type[Union[MeasData, MeasInfo, str]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[MeasData, MeasInfo, str]:
        items, _ = decode(
            data, slc.start
        )  # Sequence([Meta_cc0('len(items) != 5'), Data("")])
        if type(items) == Meta_cp0:
            print(f"DATA:type Meta_cp0:\n{items.pretty()}\n")
            return "wtf just happened"

        if type(items) == Sequence:
            if len(items) == 2:
                neid_wrapped, meas_info_wrapped = items
                return MeasData(neid_wrapped.value, meas_info_wrapped.value)
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
            return "len(items)!= 2, 4"
        return "Type!=Sequence, FileFormatVersion"


class Types(Type[List[str]]):
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> List[str]:
        x = data[slc]
        block, next = decode(x, 0, enforce_type=GraphicString)
        output = [block.pythonize()]

        while next < len(x):
            block, next = decode(x, next, enforce_type=GraphicString)
            output.append(block.pythonize())

        return output


class Values(Type[measValues]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> measValues:
        items, _ = decode(data, slc.start)
        print(f"VALUES:\n{items.pretty()}\n")
        return items
