import re
import click

# from cloudshell.recorder.snmp.snmp_recorder import SnmpRecorder
from cloudshell.recorder.snmp.snmp_service import SnmpService


class SNMPOrchestrator(object):
    DEFAULT_SYSTEM_OID = "1.3.6.1.2.1.1"

    def __init__(self, snmp_parameters, auto_detect_vendor=True, is_async=False, device_type=None,
                 template_oid_list=None, record_entire_device=False):
        self.snmp_parameters = snmp_parameters
        self._device_type = device_type
        self._is_async = is_async
        self._template_oids_list = template_oid_list
        self._auto_detect_vendor = auto_detect_vendor
        self._record_entire_device = record_entire_device

    def create_recording(self):
        recorded_data = []
        with SnmpService(self.snmp_parameters) as snmp_recorder:
            # snmp_recorder = SnmpRecorder(self.snmp_parameters)

            recorded_data.extend(snmp_recorder.create_snmp_record(oid=self.DEFAULT_SYSTEM_OID))

            if not recorded_data:
                raise Exception("Failed to initialize snmp connection")

            if self._auto_detect_vendor:
                sys_oid = [x for x in recorded_data if x.startswith("1.3.6.1.2.1.1.2")][-1]
                customer_oid_match = re.search(r"1.3.6.1.4.1.\d+", sys_oid)
                if customer_oid_match:
                    self._template_oids_list.append(customer_oid_match.group())

            snmp_record_label = "Start SNMP recording for {}".format(self.snmp_parameters.ip)
            with click.progressbar(length=len(self._template_oids_list),
                                   show_eta=False,
                                   label=snmp_record_label
                                   ) as pbar:

                for line in self._template_oids_list:
                    if line.startswith("#"):
                        continue
                    oid_line = line
                    if "#" in oid_line:
                        oid_line = re.sub(r"#+.*$", "", oid_line)
                    if oid_line.startswith("."):
                        oid_line = oid_line.strip(".\n")
                        if not re.search(r"^\d+(.\d+)*$", oid_line):
                            oid_line = re.sub(r"\D+$", "", oid_line)
                    recorded_data.extend(snmp_recorder.create_snmp_record(oid=oid_line))
                    pbar.next()

                # recorded_data.sort()
                # self.snmp_parameters.close_snmp_engine_dispatcher()
                return recorded_data