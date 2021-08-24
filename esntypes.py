"""
    This module contains the class definitions for the ASN.1 tags
"""

from dataclasses import dataclass
from datetime import date, datetime, time
from os import stat
from typing import List, Union

from x690.types import GraphicString, Integer, Type, decode
from x690.util import TypeClass, TypeNature, visible_octets


@dataclass
class MeasFileHeaderStruct:
    FileFormatVersion: str
    SenderName: str
    SenderType: int
    VendorName: str
    CollectionBeginTime: datetime


@dataclass
class MeasDataStruct:
    id: bytes  # IdUserName, IdDistinguishedName
    measInfo: bytes  # Sequence of MeasInfo


@dataclass
class MeasInfoStruct:
    measStartTime: datetime
    granularityPeriod: Integer
    measTypes: bytes  # Return bytes for MeasInfoTypes
    measValues: bytes  # Return bytes for MeasInfoValues


class Test(Type[Union[MeasFileHeaderStruct, MeasDataStruct]]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    def as_file_header(self):
        pass

    def as_measure_id(self):
        pass

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice
    ) -> Union[MeasFileHeaderStruct, MeasDataStruct]:
        print(slc)
        return data


class MeasFileHeader(Type[MeasFileHeaderStruct]):
    TAG = 0
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(
        data: bytes, slc: slice = slice(None)
    ) -> MeasFileHeaderStruct:
        FormatVersion, next = decode(data, slc.start)
        SenderName, next = decode(data, next)
        SenderType, next = decode(data, next)
        VendorName, next = decode(data, next)

        if next < slc.stop:
            CollectionBeginTime, next = decode(data, next)
        else:
            CollectionBeginTime = None

        return MeasFileHeaderStruct(
            FormatVersion, SenderName, 1, VendorName, CollectionBeginTime
        )


class HdFileFormatVersion(Type[str]):
    TAG = 0
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        value, _ = decode(data, slc.start)
        # print(value.pretty())
        return "Truncated"
        # return data[slc].decode("ascii")
        # Clashes with MeasInfoStartTime, MeasValueObjInstId


class HdSenderName(Type[str]):
    # Type should be UTF8String
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return "Truncated"
        # Return utf8 instead of ascii
        # return data[slc].decode("ascii")
        # Clashes with MeasInfoGranularityPeriod


class HdSenderType(Type[bytes]):
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class HdVendorName(Type[str]):
    TAG = 3
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return data[slc].decode("ascii")


class HdCollectionBeginTime(Type[str]):
    TAG = 4
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        date_string = data[slc].decode("ascii")
        time = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
        return time.strftime("%d/%m/%Y %H:%M:%S")  # assume TZ=Z (GMT)


class MeasData(Type[bytes]):
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        value, next = decode(data, slc.start)
        return value
        # Will collide with MeasValueResult

    def __repr__(self) -> str:
        try:
            return f"<MeasureData {len(self.value)}>"
        except TypeError:
            return ""


class MeasDataId(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class IdUsername(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class IdDistinguishedName(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MeasInfo(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MeasInfoStartTime(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MeasInfoGranularityPeriod(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MeasInfoTypes(Type[List[str]]):
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
            return f"<MeasureInfoTypes {len(self.value)}>"
        except TypeError:
            return ""


class MeasInfoValues(Type[bytes]):
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
            return f"<MeasureInfoValues {len(self.value)}>"
        except TypeError:
            return ""


class MeasType(Type[GraphicString]):
    # Obsolete since MeasInfoTypes already returns a list
    TAG = 0x19
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> GraphicString:
        result, _ = decode(data[slc], slc.start, enforce_type=GraphicString)
        return result


class MeasValue(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MeasValueObjInstId(Type[str]):
    """
    measObjInstId contains the Object Type name followed by a '.' (dot)
    followed by the individual name defined in the CP. If no individual name is
    defined a '-' (hyphen) is used, e.g. the Object Type CP does not have any
    individuals and thus the measObjInstId field contains the string “CP.-”
    """

    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class TestMeasValueObjInstId(Type[str]):
    TAG = 1  # 65
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return "Assuming ObjInstId"


class MeasValueResults(Type[bytes]):
    """
    Sequence of counter values which consists of NULL values and/or 32–
    bit unsigned integer values
    """

    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MeasValueSuspectFlag(Type[bool]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MeasResult(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class FileFooter(Type[str]):
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        date_string = data[slc].decode("ascii")
        try:
            time = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
            return time.strftime("%d/%m/%Y %H:%M:%S")  # opt; assume TZ=Z (GMT)
        except ValueError:
            return ""
            # Will collide with MeasValueSuspectFlag
