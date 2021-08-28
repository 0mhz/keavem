from dataclasses import dataclass
from datetime import date, datetime, time
from typing import List, Union

from x690.types import Sequence, Boolean, GraphicString, Integer, Type, decode
from x690.util import TypeClass, TypeNature, visible_octets

"""
    Main structure
"""


@dataclass
class MeasFileHeader:
    file_format_version: int
    sender_name: str
    sender_type: str
    vendor_name: str
    collection_begin_time: datetime


@dataclass
class MeasDataId:
    user_name: str
    distinguished_name: str


@dataclass
class MeasType:
    meas_type: str


@dataclass
class MeasResult:
    meas_result: Union[int, float, None]


@dataclass
class MeasValue:
    meas_obj_inst_id: str
    meas_results: List[MeasResult]
    suspect_flag: bool


@dataclass
class MeasInfo:
    meas_start_time: datetime
    granularity_period: int
    meas_types: List[MeasType]
    meas_values: List[MeasValue]


@dataclass
class MeasData:
    id: MeasDataId
    meas_info: List[MeasInfo]


@dataclass
class MeasDataCollection:
    file_header: MeasFileHeader
    meas_data: MeasData
    file_footer: datetime


# This might be redundant since FormatVersion is already in MeasFileHeader
# Doesn't this add an additional layer of clarity (through proper semantics)?
@dataclass
class FileFormat:
    version: int


@dataclass
class SenderType:
    sender_type: str


@dataclass
class FileFooter:
    timestamp: datetime


"""
    Header
"""


class MeasObjMeta(Type[Union[MeasFileHeader, MeasData, str]]):

    """
    <class 'collisions.Data'> expecting: collisions.Data
    in Data: <class 'collisions.FileHeader'> with value <class 'collisions.MeasFileHeader'>
    in Data: <class 'collisions.Data'> with value <class 'x690.types.Sequence'>

    This must mean that FileHeader is of type Id
    """

    TAG = 0
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice = slice(None)
    ) -> Union[MeasFileHeader, MeasData, str]:
        # Check number of items
        return "test"

    def legacy(data: bytes, slc: slice) -> Union[MeasFileHeader, MeasData, str]:
        """
        This should be handled in Data()
        try:
            items, _ = decode(data, slc.start, enforce_type=Sequence)
            # decode() fails when getting FormValObjMeta because Sequence is expected
            # Therefore, when it does not fail, there must be a sequence ahead
            id_wrapped, meas_info_wrapped = items
            print(type(id_wrapped))
            return MeasData(
                id_wrapped.value.decode("utf8"),
                meas_info_wrapped.value
            )
        except:"""
        FormatVersion, next = decode(data, slc.start)
        # if not (slc.start <= next < slc.stop):

        SenderName, next = decode(data, next)
        SenderType, next = decode(data, next)
        VendorName, next = decode(data, next)

        if next < slc.stop:
            CollectionBeginTime, next = decode(data, next)
        else:
            CollectionBeginTime = datetime(1990, 1, 1, 1, 1)

        return MeasFileHeader(
            FormatVersion,
            SenderName,
            SenderType,
            VendorName,
            CollectionBeginTime,
        )


"""
    Header objects
"""


class HdFileFormatVersion(Type[str]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return data[slc].decode("ascii")


class HdSenderName(Type[str]):
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        try:
            # same logic as before
            return data[slc].decode("ascii").rstrip()
        except:
            # item, _ = decode(data[slc])
            return "it broke"


class HdVendorName(Type[str]):
    TAG = 3
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return data[slc].decode("ascii")


class HdCollectionBeginTime(Type[datetime]):
    TAG = 4
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> datetime:
        date_string = data[slc].decode("ascii")
        time = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
        # return time.strftime("%d/%m/%Y %H:%M:%S")  # assume TZ=Z (GMT)
        return time


"""
    Measure data block
"""


class Data(Type[Union[MeasInfo, MeasData, str]]):
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[MeasInfo, MeasData, str]:
        items, _ = decode(data, slc.start, enforce_type=Sequence)
        print(items.pretty())

        if len(items) == 2:
            id_wrapped, meas_info_wrapped = items
            return MeasData(id_wrapped.value, meas_info_wrapped.value)
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
        return ""


"""
class Info(Type[List[str]]):
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

    def __repr__(self) -> str:
        try:
            return f"<Types {len(self.value)}>"
        except TypeError:
            return ""

class InfoValues(Type[bytes]):
    TAG = 3
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        # print(visible_octets(data))
        mvalue, next = decode(data, slc.start)
        output = [mvalue]

        while next < slc.stop:
            mvalue, next = decode(data, next)


            print("*** MeasInfoValues Begin ***")
            print(type(mvalue))
            print(mvalue.pretty())
            print(f"{type(mvalue[0])} : {type(mvalue[1])} : {type(mvalue[2])}")
            print(f"{mvalue[0]} : {mvalue[1]} : {mvalue[2]}")
            print("*** MeasInfoValues End *****\n")

            output.append(mvalue)

        return output

    def __repr__(self) -> str:
        try:
            return f"<Values {len(self.value)}>"
        except TypeError:
            return ""
"""

"""
    Footer
    FileFooter in StypeFooterObjMeta()
"""


"""
    Meta
"""


@dataclass
class Eidel:
    content: bytes


class FormValObjMeta(Type[Union[FileFormat, Eidel]]):

    TAG = 0
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[FileFormat, Eidel]:
        if not data[slc]:
            return Eidel(data)
        item, _ = decode(data, slc.start)
        # print(f"FVOM Item:{item.pretty()}")
        # return appropriate dataclass for MeasValues?
        return FileFormat(1)


class MultObjMeta(Type[Union[SenderType, MeasValue, FileFooter, str]]):
    # Sendertype, MeasValue, FileFooter
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[SenderType, MeasValue, FileFooter, str]:
        try:
            item = data[slc].decode("ascii")
            if len(item) >= 14:
                time = datetime.strptime((item[0:14]), "%Y%m%d%H%M%S")
                return FileFooter(time)
            if not item:
                return SenderType("1")
        except:
            items, _ = decode(data, slc.start, enforce_type=Sequence)
            print("bla")
            return "exc"
        return ""
