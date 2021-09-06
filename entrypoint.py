from x690 import decode

from keavem import decode as keavem
from keavem.structure import MeasDataCollection

filename = "tests/data/file.asn1"
with open(filename, "rb") as data:
    data = data.read()
result, _ = decode(data)
meas_file_header, meas_data, meas_file_footer = result

print(MeasDataCollection(meas_file_header, meas_data, meas_file_footer))
