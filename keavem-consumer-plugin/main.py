import logging
import time
from os.path import basename

from kraken import __version__
from kraken.config import Config
from kraken.helpers import delete_file, fetch_remote_file, get_local_file_path
from kraken.logging import enrich_log
from kraken.plugins.consumers.generic import GenericPlugin, GenericResult
from kraken.plugins.consumers.keavem.model.decode import decode
from kraken.plugins.consumers.keavem.model.parse import parse
from kraken.plugins.consumers.keavem.model.structure import MeasDataCollection
from x690 import decode as x_decode

LOG = logging.getLogger(__name__)


class Keavem(GenericPlugin):
    def __init__(self, *args, **kwargs):
        GenericPlugin.__init__(self, *args, **kwargs)

        # Used for log enrichement
        self.extra = {"intent": "2G asn decoding"}

        conf = Config.create()
        self.conf_main = conf.plugins.keavem

    def handle_message(self, event):
        """
        This is the method that will be submitted in the Processor thread pool.

        :param event: Event which contains data to be processed.
        """
        evt_data = event.get("data")

        self.extra["base_event"] = event

        try:
            start_time = time.time()

            file_path = evt_data.get("file_path", "").strip()
            host = evt_data.get("host", "")
            local_file_path = get_local_file_path(file_path, host, self.extra)

            if not local_file_path:
                return 1

            if host:
                self.extra["file_name"] = basename(file_path)
                self.extra["local_file_name"] = basename(local_file_path)
                connection_port = evt_data.get("port", "22")

                fetched = fetch_remote_file(
                    self.conf_main.enm_user,
                    self.conf_main.enm_password,
                    host,
                    connection_port,
                    file_path,
                    local_file_path,
                    control_path=True,
                )

                if not fetched:
                    LOG.error(
                        "File was not fetched, skip this file...",
                        extra=enrich_log(self.extra),
                    )
                    return 1

            try:
                with open(local_file_path, "rb") as data:
                    data = data.read()

                result, _ = x_decode(data)
                meas_file_header, meas_data, meas_file_footer = result

                metrics = parse(
                    MeasDataCollection(meas_file_header, meas_data, meas_file_footer)
                )  # => [KeavemMetric]
            except Exception as exc:
                LOG.error(
                    "Keavem: file with path %s can't be parsed !",
                    local_file_path,
                    exc_info=True,
                    extra=enrich_log(self.extra),
                )
                return 1
            finally:
                if host:
                    # in this case, file has been fetched, needs to be deleted.
                    delete_file(local_file_path)

            lines = [metric.as_influx_string() for metric in metrics]

            result = GenericResult(data=[line for line in lines if line])

            self.extra["exec_time"] = time.time() - start_time
            LOG.info(
                "Execution finished in %s" % (time.time() - start_time),
                extra=enrich_log(self.extra),
            )

            return result

        except Exception as exc:
            # Global fallback error handler. I don't want the whole instance to
            # crash.
            LOG.exception(
                "Unexpected error occured inside snmp_trap_handler plugin.",
                exc_info=True,
                extra=enrich_log(self.extra),
            )
            return 1
