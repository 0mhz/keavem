"""
    This module contains the class definitions for the ASN.1 tags
"""

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import List

from x690.types import (
    GeneralizedTime,
    GraphicString,
    Integer,
    Type,
    Utf8String,
    decode,
)
from x690.util import TypeClass, TypeNature, decode_length, visible_octets


@dataclass
class MeasFileHeaderStruct:
    FileFormatVersion: str
    SenderName: str
    SenderType: int
    VendorName: str
    CollectionBeginTime: datetime


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
        return "Truncated"


class HdSenderName(Type[str]):
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return "Truncated"


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
    # Sequence of: Id, Info
    TAG = 1  # Tag = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        value, next = decode(data, slc.start)
        """
        print("------ MeasData Begin ------")
        print(value[0])
        print(value[1])
        print("------ MeasData End --------")
        """
        return value

    def __repr__(self) -> str:
        """
        if self.value:
            return f"<MeasureData {len(self.value)}>"
        else:
            return "No length"
        """
        try:
            return f"<MeasureData {len(self.value)}>"
        except ValueError:
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


class MeasInfoValues(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MeasType(Type[str]):
    TAG = 0x19
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MeasValue(Type[bytes]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MeasValueObjInstId(Type[str]):
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MeasValueResults(Type[bytes]):
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
            # return date_string
        except ValueError:
            return ""
