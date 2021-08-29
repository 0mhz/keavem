from typing import List, Union
from x690.types import Sequence, Type, decode
from x690.util import TypeClass, TypeNature
from dataclasses import dataclass

block = b"0\x81\x92aJ0H\x04\x08acmecorp0&b\x110\x0f\x04\x04John\x04\x03Doe\x02\x0209b\x110\x0f\x04\x04Jane\x04\x03Doe\x02\x0209c\x140\x12\x04\x04some\x04\x07example\x02\x01\x0caD0B\x04\x0banothercorp0,b\x140\x12\x04\x05Timon\x04\x05Baker\x02\x02\r\x05b\x140\x12\x04\x06Random\x04\x04Name\x02\x02\x11\\c\x050\x03\x02\x01\r"


@dataclass
class Address:
    line_1: str
    line_2: str
    floor: int


@dataclass
class LocalIdentifier:
    company_id: int


@dataclass
class Employee:
    first_name: str
    last_name: str
    monthly_salary: int


@dataclass
class Company:
    name: str
    employees: List[Employee]
    meta: Union[Address, LocalIdentifier]


class CompanyType(Type[Company]):
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Company:
        items, _ = decode(data, slc.start, enforce_type=Sequence)
        name_wrapped, employees_wrapped, meta_wrapped = items
        return Company(
            name_wrapped.value.decode("utf8"),
            # list comprehension
            [e.value for e in employees_wrapped.value],
            meta_wrapped.value,
        )


class EmployeeType(Type[Employee]):
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Employee:
        items, _ = decode(data, slc.start, enforce_type=Sequence)
        fname_wrapped, lname_wrapped, salary_wrapped = items
        return Employee(
            fname_wrapped.value.decode("utf8"),
            lname_wrapped.value.decode("utf8"),
            salary_wrapped.value,
        )


class ObjectsType(Type[Union[Address, LocalIdentifier]]):
    TYPECLASS = TypeClass.APPLICATION
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 3

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[Address, LocalIdentifier]:
        items, _ = decode(data, slc.start, enforce_type=Sequence)
        if len(items) == 3:
            return Address(
                items[0].value.decode("utf8"),
                items[1].value.decode("utf8"),
                items[2].value,
            )
        return LocalIdentifier(items[0].value)


result, _ = decode(block, enforce_type=Sequence)
company_1: Company = result[0].value
company_2: Company = result[1].value

print(company_1)
"""
print(company_1.name)
print(company_1.employees[0].first_name)

print(company_1.meta.company_id)  # <- Shows a typing error because "meta"
                                  #    could be of type "Address" which does
                                  #    not have this attribute

if isinstance(company_1.meta, LocalIdentifier):
    print(company_1.meta.company_id)  # <- Typing error is gone.
 """
