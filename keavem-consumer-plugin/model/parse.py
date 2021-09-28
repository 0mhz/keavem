from datetime import datetime

from kraken.plugins.consumers.generic import InfluxMetric
from kraken.plugins.consumers.keavem.model.exceptions import (
    MeasurementTypeValueCountDiffer,
)
from kraken.plugins.consumers.keavem.model.structure import MeasFileHeader


class KeavemMetric(InfluxMetric):
    pass


def parse_header(meas_file_header):
    file_format_version_decoded = int.from_bytes(
        meas_file_header.file_format_version, "big"
    )
    sender_name_stripped = meas_file_header.sender_name.decode("ascii").rstrip()
    collection_begin_time = int(
        datetime.timestamp(meas_file_header.collection_begin_time) * 1000000000
    )
    return MeasFileHeader(
        file_format_version_decoded,
        sender_name_stripped,
        meas_file_header.sender_type,
        meas_file_header.vendor_name,
        collection_begin_time,
    )


def parse_footer(meas_file_footer):
    return datetime.timestamp(meas_file_footer)


def parse(data_collection):
    """
    TODO
    """
    metrics = []

    header = parse_header(data_collection.file_header.value)
    meas_info = data_collection.meas_data.value.meas_info

    for items in meas_info:
        start_time = int(
            datetime.timestamp(
                datetime.strptime(
                    items.meas_start_time.decode("ascii"), "%Y%m%d%H%M%SZ"
                )
            )
            * 1000000000
        )
        types = items.meas_types
        for value in items.meas_values:
            object_instance_id = value.meas_obj_inst_id
            measurement_results = value.meas_results
            suspect_flag = value.suspect_flag

            if len(types) != len(measurement_results):
                raise MeasurementTypeValueCountDiffer(
                    f"Length of types: {len(types)} different than length of measurement results: {len(measurement_results)}"
                )

            field_set = dict(zip(types, measurement_results))
            tag_set = {
                "suspect": suspect_flag,
                "sender_name": header.sender_name,
            }

            metrics.append(
                KeavemMetric(
                    object_instance_id,
                    tag_set,
                    field_set,
                    start_time,
                )
            )

    return metrics
