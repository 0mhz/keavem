from dataclasses import dataclass
from datetime import datetime
from typing import List, Sequence, Union

from x690.types import Sequence


@dataclass
class MeasFileFooter:
    time: datetime
    tzone: str


@dataclass
class MeasResult:
    meas_result: Union[int, float, None]


@dataclass
class suspectFlag:
    value: bool


@dataclass
class measResults:
    results: List[MeasResult]


@dataclass
class measObjInstId:
    value = str


@dataclass
class MeasValue:
    meas_obj_inst_id: measObjInstId
    meas_results: measResults
    suspect_flag: bool


@dataclass
class MeasType:
    meas_type: str


@dataclass
class measValues:
    values = List[MeasValue]


@dataclass
class measTypes:
    values = List[MeasType]


@dataclass
class measTypesLegacy:
    values = List[str]


@dataclass
class granularityPeriod:
    value: int


@dataclass
class measStartTime:
    time: datetime
    tzone: str


@dataclass
class MeasInfo:
    meas_start_time: measStartTime
    granularity_period: granularityPeriod
    meas_types: measTypes
    meas_values: measValues


@dataclass
class nEDistinguishedName:
    value: str  # None


@dataclass
class nEUserName:
    value: str


@dataclass
class NEId:
    ne_user_name: nEUserName
    ne_distinguished_name: nEDistinguishedName


@dataclass
class measInfo:
    values: List[MeasInfo]


@dataclass
class nEId:
    value: NEId


@dataclass
class MeasData:
    ne_id: NEId
    meas_info: measInfo


@dataclass
class SenderType:
    value: str


@dataclass
class collectionBeginTime:
    time: datetime
    tzone: str


@dataclass
class vendorName:
    value: str


@dataclass
class senderType:
    value: SenderType


@dataclass
class senderName:
    value: str


@dataclass
class fileFormatVersion:
    value: int


@dataclass
class MeasFileHeader:
    file_format_version: fileFormatVersion
    sender_name: senderName
    sender_type: senderType
    vendor_name: vendorName
    collection_begin_time: collectionBeginTime


@dataclass
class measFileFooter:
    value: MeasFileFooter


@dataclass
class measData:
    value: MeasData


@dataclass
class measFileHeader:
    value: MeasFileHeader


@dataclass
class MeasDataCollection:
    file_header: MeasFileHeader
    meas_data: MeasData
    file_footer: MeasFileFooter


@dataclass
class CatchMetaError:
    item: Union[int, bytes, str, List[bytes], List[str], Sequence]