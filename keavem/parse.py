import datetime

from keavem.structure import MeasData, MeasDataCollection, MeasFileHeader


def parse_header(meas_file_header):
    print(meas_file_header)
    file_format_version_decoded = int.from_bytes(
        meas_file_header.file_format_version, "big"
    )
    sender_name_stripped = meas_file_header.sender_name.decode("ascii").rstrip()
    collection_begin_time = datetime.datetime.timestamp(
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


def parse_footer(meas_file_footer):
    return datetime.datetime.timestamp(meas_file_footer)


def parse(data_collection):
    header = parse_header(data_collection.file_header.value)
    data = data_collection.meas_data.value
    footer = parse_footer(data_collection.file_footer.value)
    print(header)
    print(footer)

    influxdb_tags = []
    influxdb_measurements = []


class parse_headerio:
    pass
