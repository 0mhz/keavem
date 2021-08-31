from x690.types import Type, decode
from x690.util import TypeClass, TypeNature


class StrCodec(Type[str]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> str:
        sender_name_wrapped, _ = decode(data, slc.start)
        for i in Type.all():
            print(i)
        return sender_name_wrapped
