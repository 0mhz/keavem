from dataclasses import dataclass
from datetime import datetime
from typing import List, Union


@dataclass
class MeasValue:
    meas_obj_inst_id: str
    meas_results: List[Union[int, float, None]]
    suspect_flag: bool


@dataclass
class measTypesLegacy:
    values = List[str]


@dataclass
class MeasInfo:
    meas_start_time: datetime
    granularity_period: int
    meas_types: List[str]
    meas_values: List[MeasValue]


@dataclass
class NEId:
    ne_user_name: str
    ne_distinguished_name: str


@dataclass
class MeasData:
    ne_id: NEId
    meas_info: List[MeasInfo]


@dataclass
class MeasFileHeader:
    file_format_version: int
    sender_name: str
    sender_type: str
    vendor_name: str
    collection_begin_time: datetime


@dataclass
class MeasDataCollection:
    file_header: MeasFileHeader
    meas_data: MeasData
    file_footer: datetime
