import re
import click
from pysnmp.proto.errind import RequestTimedOut

from cloudshell.recorder.snmp.snmp_service import SnmpService


class SNMPOrchestrator(object):
    SYS_OBJECT_ID_OID = "1.3.6.1.2.1.1.2"
    ROOT_VENDOR_OID = "1.3.6.1.4.1"

    def __init__(self, snmp_parameters, auto_detect_vendor=True, is_async=False, device_type=None,
                 template_oid_list=None, record_entire_device=False):
        self.snmp_parameters = snmp_parameters
        self._device_type = device_type
        self._is_async = is_async
        self._template_oids_list = template_oid_list or []
        self._auto_detect_vendor = auto_detect_vendor
        self._record_entire_device = record_entire_device

    def create_recording(self):
        recorded_data = []
        sys_obj_id = None
        with SnmpService(self.snmp_parameters) as snmp_recorder:
            try:
                sys_obj_list = snmp_recorder.create_snmp_record(oid=self.SYS_OBJECT_ID_OID, get_single_value=True)
                if sys_obj_list:
                    sys_obj_id = sys_obj_list[0]
            except RequestTimedOut as e:
                # ToDo add logger here
                raise Exception("Failed to initialize snmp connection: \n{}".format(e))

            if self._auto_detect_vendor:
                customer_oid_match = re.search(r"{0}.\d+".format(self.ROOT_VENDOR_OID), sys_obj_id or "")
                if customer_oid_match:
                    self._template_oids_list.append(customer_oid_match.group())
                else:
                    click.secho("Unable to detect target device manufacturer.")
                    self._template_oids_list.append(self.ROOT_VENDOR_OID)

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
                    oid_line = oid_line.strip("\n")
                    if not re.search(r"^\d+(.\d+)*$", oid_line):
                        oid_line = re.sub(r"^\.*|\D+$", "", oid_line)
                        if not re.search(r"^\d+(.\d+)*$", oid_line):
                            continue
                    try:
                        recorded_data.extend(snmp_recorder.create_snmp_record(oid=oid_line))
                    except KeyboardInterrupt:
                        raise
                    except:
                        pass
                    pbar.next()

                return recorded_data
