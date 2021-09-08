from collections import OrderedDict
from datetime import datetime

from keavem.exceptions import MeasurementTypeValueCountDiffer
from keavem.structure import MeasData, MeasDataCollection, MeasFileHeader


def parse_header(meas_file_header):
    file_format_version_decoded = int.from_bytes(
        meas_file_header.file_format_version, "big"
    )
    sender_name_stripped = meas_file_header.sender_name.decode("ascii").rstrip()
    collection_begin_time = datetime.timestamp(
        meas_file_header.collection_begin_time
    )
    return MeasFileHeader(
        file_format_version_decoded,
        sender_name_stripped,
        meas_file_header.sender_type,
        meas_file_header.vendor_name,
        collection_begin_time,
    )


def parse_data(meas_data):
    pass
    # Shall return a list of
    meas_info = meas_data.meas_info
    print(meas_info)


def parse_footer(meas_file_footer):
    return datetime.timestamp(meas_file_footer)


def parse(data_collection):
    header = parse_header(data_collection.file_header.value)
    data = data_collection.meas_data.value
    meas_info = data.meas_info
    footer = parse_footer(data_collection.file_footer.value)

    for items in meas_info:
        start_time = datetime.timestamp(
            datetime.strptime(
                items.meas_start_time.decode("ascii"), "%Y%m%d%H%M%S%f%z"
            )
        )
        types = items.meas_types
        values = items.meas_values
        for value in values:
            object_instance_id = value.meas_obj_inst_id
            measurement_results = value.meas_results
            suspect_flag = value.suspect_flag

            if len(types) != len(measurement_results):
                raise MeasurementTypeValueCountDiffer(
                    f"Length of types: {len(types)} different than length of measurement results: {len(measurement_results)}"
                )

            print(
                f"{object_instance_id},suspect={suspect_flag},sender_name={header.sender_name}",
                end=" ",
            )
            counters = OrderedDict(zip(types, measurement_results))
            for key, value in counters.items():
                # Negative slice method is fastest compared to index and enumerate method
                # TODO: Remove OrderedDict: An OrderedDict is no longer necessary as dictionary keys are
                # officially ordered in insertion order as of Python 3.7 (unofficially in 3.6).
                # https://stackoverflow.com/questions/16125229/last-key-in-python-dictionary
                if key == list(counters.keys())[-1]:
                    print(f"{key}={value}", end=" ")
                else:
                    print(f"{key}={value}", end=",")
            print(f"{start_time}")
