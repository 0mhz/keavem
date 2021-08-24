"""
    This module contains the class definitions for the ASN.1 tags that will be
    used to decode the header in order to know which specific sender type the
    BSC is using to enable an automatic parsing of the syntax
"""

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import List

from x690.types import (
    GeneralizedTime,
    GraphicString,
    Integer,
    Null,
    Type,
    Utf8String,
    decode,
)
from x690.util import TypeClass, TypeNature, decode_length, visible_octets


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


class FileHeader(Type[FileHeaderInfo]):
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
        # print(visible_octets(data))
        # print(decode_length(data, 1))
        FormatVersion, next = decode(data, slc.start)
        SenderName, next = decode(data, next)
        SenderType, next = decode(data, next)
        SenderType = 1
        VendorName, next = decode(data, next)
        if next < slc.stop:
            CollStartTime, next = decode(data, next)
        else:
            CollStartTime = None
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
        # return "FormatVersion truncated due to tag clash in (presumably) MeasureStartTime"
        return "etypes:FormatVersion()"


class SenderName(Type[str]):
    TAG = 1
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        return "etypes:SenderName()"  # clash with GranularityTime
        # return data[slc].decode("ascii")


class FormVerMeasTime(Type[bytes]):
    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        return super().decode_raw(data, slc=slc)

    def as_format_version(self):
        print(self.value)
        return FormatVersion("Test")

    def as_measure_start_time(self):
        print(self.value)
        return MeasureStartTime(self.value)


class SendNameGranTime(Type[bytes]):
    pass


"""
class Foo(Type[bytes]):
    def decode_raw(...):
        return <raw-bytes from the slice>
    def as_file_format_version(self):
       ... process self.value ... (which contains the raw-bytes)
       return FileFormatVersion(...)
    def as_measure_start_time(self):
        ...
"""


class Test(Type[bytes]):
    TAG = 3
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> bytes:
        x, next = decode(data, slc.start)
        output = [x]

        while next < slc.stop:
            x, next = decode(data, next)
            print("******** MeasureInfo[Cont, Constr, 3]: Begin ********")
            print(type(x))
            print(x.pretty())
            print("******** MeasureInfo[Cont, Constr, 3]: End ******")
            output.append(x)
        return output

        print(type(x))
        print(slc)
        print(slc.stop - slc.start)
        print(next)
        x, next = decode(data, next)
        print(type(x))
        x, next = decode(data, next)
        print(type(x))
        return b"Hallo"
        # return str(x).encode("ascii")[:5]


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


class MeasureStartTime(Type[str]):
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
        value, next = decode(data, slc.start)
        """ print("#### MEASUREDATA ###")
        print(value[0])
        print(value[1])
        print("#### ########### ###")
        """
        return value

    def __repr__(self) -> str:
        if self.value:
            return f"<MeasureData {len(self.value)}>"
        else:
            return "No length"

        # try:
        #    return f"<MeasureData {len(self.value)}>"
        # except ValueError:
        #    return ""


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


class MeasureGranularityPeriod(Type[bytes]):
    # Integer
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class MTypes(Type[List[str]]):
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


"""
class MTypes(Type[List[Type[bytes]]]):
    # Sequence of MType
    TAG = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> List[Type[bytes]]:
        start_index = slc.start or 0
        item: Type[bytes]
        item, next_pos = decode(data, start_index)
        items: List[Type[bytes]] = [item]
        end = slc.stop or len(data)
        while next_pos < end:
            item, next_pos = decode(data, next_pos)
            items.append(item)
        return items
"""


class MValues(Type[bytes]):
    # Sequence of MValue
    TAG = None
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]


class MType(Type[str]):
    TAG = 0x19
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


class FileFooter(Type[str]):
    # 0x82
    TAG = 2  # Tag = 2
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        date_string = data[slc].decode("ascii")
        try:
            time = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
            return time.strftime("%d/%m/%Y %H:%M:%S")  # opt; assume TZ=Z (GMT)
        #            return date_string
        except ValueError:
            return ""


class TimeStamp(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]


class PrintableString(Type[bytes]):
    TAG = Null
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
