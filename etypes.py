"""
    This module contains the class definitions for the ASN.1 tags that will be
    used to decode the header in order to know which specific sender type the
    BSC is using to enable an automatic parsing of the syntax
"""

from x690.types import GeneralizedTime, Integer, Null, Type, Utf8String
from x690.util import TypeClass, TypeNature


class DataCollection(Type[bytes]):
    # Sequence of: FileHeader, Sequence of MeasureData and FileFooter
    TAG = 0x30
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class FileHeader(Type[bytes]):
    # Sequence of:
    # FormatVersion, Sendername, Sendertype, Vendorname, CollectionStartTime
    # actually TAG = 0xa0 but 0x00 somehow yields a better result in decode()
    TAG = 0x00
    # DEC 160
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class FormatVersion(Type[Integer]):
    TAG = 0x80
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class SenderName(Type[Utf8String]):
    TAG = 0x81
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class SenderType(Type[bytes]):
    # String length 0-8
    # TAG = 0x82 Clash with FileFooter
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class VendorName(Type[bytes]):
    # String length 0-32
    TAG = 0x83
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class LogStartTime(Type[str]):
    # Actually a timestamp of type GeneralizedTime (presumably X.690 spec.)
    TAG = 0x84
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(2, -1)) -> str:
        data = data[slc].decode("ascii")
        return GeneralizedTime(data)


class MeasureData(Type[bytes]):
    # Sequence of: Id, Info
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class Id(Type[bytes]):
    # Sequence of Username, DistinguishedName
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class Username(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString


class DistinguishedName(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString


class MInfo(Type[bytes]):
    # Sequence of MStartTime, GranulPeriod, MTypes, MValues
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MStartTime(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(None)) -> str:
        return TimeStamp.get_time(data)


class MGranulPeriod(Type[bytes]):
    # Integer
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MTypes(Type[bytes]):
    # Sequence of MType
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MValues(Type[bytes]):
    # Sequence of MValue
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MType(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString


class MValue(Type[bytes]):
    # Sequence of ObjectInstanceId, Seq. of Result, SuspectFlag
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class ObjectInstanceId(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return PrintableString


class Result(Type[bytes]):
    # CHOICE of Integer, Real, None
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    # NATURE = [TypeNature.CONSTRUCTED]


class SuspectFlag(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return super().decode_raw(data, slc=slc)
        # Return Boolean


class FileFooter(Type[bytes]):
    TAG = 0x82
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(None)) -> str:
        return TimeStamp.get_time(data)

    def use_gentime(data: bytes, slc: slice = slice(2, -1)) -> str:
        data = data[slc].decode("ascii")
        return GeneralizedTime(data)


class TimeStamp(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

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


class PrintableString(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
