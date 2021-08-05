from x690.types import Type
from x690.util import *


class MeasFileFooter(Type[bytes]):
    TAG = 0x82
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]

    @staticmethod
    def decode_raw(data: bytes, slc: slice = slice(2, -1)) -> str:
        data = data[slc].decode("ascii")
        return data

    # This has been made in the middle of the night.
    # Probably decode once and return object as a tuple(time, timezone)
    def get_time(data: bytes, slc: slice = slice(2, 16)) -> str:
        data = data[slc].decode("ascii")
        return data

    def get_timezone(data: bytes, slc: slice = slice(16, -1)) -> str:
        data = data[slc].decode("ascii")
        return data
