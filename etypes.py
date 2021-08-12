"""
    This module contains the class definitions for the ASN.1 tags that will be
    used to decode the header in order to know which specific sender type the
    BSC is using to enable an automatic parsing of the syntax
"""

from dataclasses import dataclass
from datetime import date, datetime, time

from x690.types import GeneralizedTime, Integer, Null, Type, Utf8String, decode
from x690.util import TypeClass, TypeNature


class DataCollection(Type[bytes]):
    # Sequence of: FileHeader, Sequence of MeasureData and FileFooter
    TAG = 0x30
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


@dataclass
class FileHeaderInfo:
    FormatVersion: str
    SenderName: str
    SenderType: int
    VendorName: str
    CollStartTime: datetime


class FileHeader(Type[str]):
    # Sequence of:
    # FormatVersion, Sendername, Sendertype, Vendorname, CollectionStartTime
    # actually TAG = 0xa0, dec 160
    TAG = 0
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    # @staticmethod
    # def decode_raw(data: bytes, slc: slice) -> dict:
    #     FormatVersion, next = decode(data, slc.start)
    #     SenderName, next = decode(data, next)
    #     SenderType, next = decode(data, next)
    #     VendorName, next = decode(data, next)
    #     CollStartTime, next = decode(data, next)
    #     return {"FormatVersion":FormatVersion, "SenderName":SenderName, "SenderType": SenderType, "VendorName": VendorName, "CollStartTime": CollStartTime}

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(None)) -> FileHeaderInfo:
        FormatVersion, next = decode(data, slc.start)
        SenderName, next = decode(data, next)
        SenderType, next = decode(data, next)
        SenderType = 1
        VendorName, next = decode(data, next)
        CollStartTime, next = decode(data, next)
        """
        print(FormatVersion.pretty())
        print(SenderName.pretty())
        print(VendorName.pretty())
        print(CollStartTime.pretty())
        """
        return FileHeaderInfo(
            FormatVersion, SenderName, SenderType, VendorName, CollStartTime
        )


# actually its an integer
class FormatVersion(Type[str]):
    TAG = 0
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return "FormatVersion truncated due to tag clash in (presumably) MeasureStartTime"


class SenderName(Type[str]):
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return "Sendername truncated due to tag clash in (presumably) GranularityTime"


class SenderType(Type[bytes]):
    # String length 0-8
    # TAG = 0x82 Clash with FileFooter
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class VendorName(Type[str]):
    # String length 0-32
    TAG = 3
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return data[slc].decode("ascii")


class CollStartTime(Type[str]):
    TAG = 4
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        date_string = data[slc].decode("ascii")
        time = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
        return time.strftime("%d/%m/%Y %H:%M:%S")  # opt; assume TZ=Z (GMT)


class MeasureData(Type[bytes]):
    # Sequence of: Id, Info
    TAG = 1  # Tag = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        value, next = decode(data[slc], slc.start)
        print(value.pretty())

        while next < len(data):
            value, next = decode(data, next)
            print(value.pretty())

        return "Output truncated"

    """
    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        id, next = decode(data[slc], slc.start)
        print(id.pretty())
        return "bla"
    """
    """
    def pretty(self, depth: int) -> str:
        #return super().pretty(depth=depth)
        return "MeasureData truncated (etypes.py:108)"
    """


class Id(Type[bytes]):
    # Sequence of Username, DistinguishedName
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class Username(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    """
    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString
    """


class DistinguishedName(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    """
    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString
    """


class MInfo(Type[bytes]):
    # Sequence of MStartTime, GranulPeriod, MTypes, MValues
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MStartTime(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    """
    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(None)) -> str:
        return TimeStamp.get_time(data)
    """


class MGranulPeriod(Type[bytes]):
    # Integer
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MTypes(Type[bytes]):
    # Sequence of MType
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MValues(Type[bytes]):
    # Sequence of MValue
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MType(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    """
    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString
    """


class MValue(Type[bytes]):
    # Sequence of ObjectInstanceId, Seq. of Result, SuspectFlag
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class ObjectInstanceId(Type[str]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        pass
        # Return PrintableString


class Result(Type[bytes]):
    # CHOICE of Integer, Real, None
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    # NATURE = [TypeNature.CONSTRUCTED]


class SuspectFlag(Type[bool]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bool:
        pass
        # Return Boolean


class FileFooter(Type[bytes]):
    # 0x82
    TAG = 2  # Tag = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        date_string = data[slc].decode("ascii")
        time = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
        return time.strftime("%d/%m/%Y %H:%M:%S")  # opt; assume TZ=Z (GMT)

    """
    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(None)) -> str:
        return TimeStamp.get_time(data)

    def use_gentime(data: bytes, slc: slice = slice(2, -1)) -> str:
        data = data[slc].decode("ascii")
        return GeneralizedTime(data)
    """


class TimeStamp(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    """
    # This has been made in the middle of the night.
    # Probably decode once and return object as a tuple(time, timezone)
    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(2, -1)) -> str:
        data = data[slc].decode("ascii")
        return data

    def get_time(data: bytes, slc: slice = slice(2, 16)) -> str:
        data = data[slc].decode("ascii")
        return data

    def get_timezone(data: bytes, slc: slice = slice(16, -1)) -> str:
        data = data[slc].decode("ascii")
        return data
    """


class PrintableString(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
