import sys
from datetime import datetime

from keavem.exceptions import MeasurementTypeValueCountDiffer
from keavem.structure import MeasFileHeader


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


def parse(data_collection, **kwargs):
    outputfile = kwargs.get("output")
    if outputfile:
        outstream = open(outputfile, "w")
    else:
        outstream = sys.stdout
    header = parse_header(data_collection.file_header.value)
    meas_info = data_collection.meas_data.value.meas_info
    # footer = parse_footer(data_collection.file_footer.value)

    for items in meas_info:
        start_time = int(
            datetime.timestamp(
                datetime.strptime(
                    items.meas_start_time.decode("ascii"), "%Y%m%d%H%M%S%f%z"
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

            counters = dict(zip(types, measurement_results))
            measurement_tagset = f"{object_instance_id},suspect={suspect_flag},sender_name={header.sender_name} "
            print(f"{measurement_tagset}", end="", file=outstream)

            for key, value in counters.items():
                # Negative slice method is fastest compared to index and enumerate method
                if key == list(counters.keys())[-1]:
                    field_set = f"{key}={value} "
                    print(field_set, end="", file=outstream)
                else:
                    field_set_last = f"{key}={value},"
                    print(field_set_last, end="", file=outstream)
            print(f"{start_time}", end="\n", file=outstream)
