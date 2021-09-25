import argparse

from keavem.decode import decode
from keavem.parse import parse
from keavem.structure import MeasDataCollection
from x690 import decode

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-i",
    "--input",
    required=True,
    action="store",
    dest="input_file",
    help="Path to a file encoded in ASN.1",
)
argparser.add_argument(
    "-o",
    "--output",
    action="store",
    dest="output_file",
    help="Path where the parsed file will be stored",
)
args = argparser.parse_args()

with open(args.input_file, "rb") as data:
    data = data.read()
result, _ = decode(data)
meas_file_header, meas_data, meas_file_footer = result
parse(
    MeasDataCollection(meas_file_header, meas_data, meas_file_footer),
    output=args.output_file,
)
