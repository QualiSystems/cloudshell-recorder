# from recorder.file_service.file_service import create_output_archive
from cloudshell.recorder.file_service.file_service import create_output_archive

from cloudshell.recorder.model.snmp_v2_parameters import SnmpV2Parameters
from cloudshell.recorder.model.snmp_v3_parameters import SnmpV3Parameters
from cloudshell.recorder.snmp.snmp_orchestrator import SNMPOrchestrator
from cloudshell.recorder.tools.snmp_tools import ENTIRE_SNMP_OID_LIST, \
    DEFAULT_SNMP_OID_LIST


class RecorderOrchestrator(object):
    def __init__(self, ip, recording_type, destination_path):
        self._ip = ip
        self._recording_type = recording_type
        self._destination_path = destination_path

    def new_recording(self, cli_user=None,
                      cli_password=None,
                      cli_enable_password=None,
                      snmp_community=None,
                      snmp_user=None,
                      snmp_password=None,
                      snmp_private_key=None,
                      snmp_auth_protocol=None,
                      snmp_priv_protocol=None,
                      snmp_record=None,
                      snmp_timeout=2000,
                      snmp_retries=2,
                      snmp_bulk="None",
                      snmp_bulk_repetitions=25,
                      snmp_auto_detect_vendor="true"):

        cli_recording = None
        snmp_recording = None
        if cli_user or cli_password:
            cli_recording = self._new_cli_recording(cli_user=cli_user, cli_password=cli_password,
                                                    cli_enable_password=cli_enable_password)
        if snmp_community or snmp_user:
            snmp_recording = self._new_snmp_recording(snmp_community=snmp_community,
                                                      snmp_user=snmp_user, snmp_password=snmp_password,
                                                      snmp_private_key=snmp_private_key,
                                                      snmp_auth_protocol=snmp_auth_protocol,
                                                      snmp_priv_protocol=snmp_priv_protocol,
                                                      snmp_record=snmp_record,
                                                      snmp_timeout=snmp_timeout,
                                                      snmp_retries=snmp_retries,
                                                      snmp_bulk=snmp_bulk,
                                                      snmp_bulk_repetitions=snmp_bulk_repetitions,
                                                      snmp_auto_detect_vendor=snmp_auto_detect_vendor)
        path = create_output_archive(cli_recording, snmp_recording, self._destination_path, self._ip)
        print "Output file path: {}".format(path)
        print "Recording Completed."

    def _new_snmp_recording(self,
                            snmp_community=None,
                            snmp_user=None,
                            snmp_port=161,
                            snmp_password=None,
                            snmp_private_key=None,
                            snmp_auth_protocol="NONE",
                            snmp_priv_protocol="NONE",
                            snmp_record=None,
                            snmp_auto_detect_vendor="true",
                            is_ipv6=False,
                            snmp_timeout=2000,
                            snmp_retries=2,
                            snmp_bulk="None",
                            snmp_bulk_repetitions=25,
                            continue_on_errors=0,
                            v3_context_engine_id=None,
                            v3_context=''):
        snmp_bulk_flag = snmp_bulk.lower() == "true"
        auto_detect_vendor = snmp_auto_detect_vendor.lower() == "true"
        if snmp_user:
            snmp_parameters = SnmpV3Parameters(self._ip, v3_user=snmp_user, v3_auth_key=snmp_password,
                                               v3_priv_key=snmp_private_key, v3_auth_proto=snmp_auth_protocol,
                                               v3_priv_proto=snmp_priv_protocol, port=snmp_port,
                                               is_ipv6=is_ipv6, timeout=snmp_timeout,
                                               retry_count=snmp_retries, get_bulk_flag=snmp_bulk_flag,
                                               continue_on_errors=continue_on_errors,
                                               get_bulk_repetitions=snmp_bulk_repetitions,
                                               v3_context_engine_id=v3_context_engine_id,
                                               v3_context=v3_context)
        else:
            snmp_parameters = SnmpV2Parameters(self._ip, snmp_community=snmp_community, port=snmp_port,
                                               is_ipv6=is_ipv6, timeout=snmp_timeout,
                                               retry_count=snmp_retries, get_bulk_flag=snmp_bulk_flag,
                                               continue_on_errors=continue_on_errors,
                                               get_bulk_repetitions=snmp_bulk_repetitions,
                                               v3_context_engine_id=v3_context_engine_id,
                                               v3_context=v3_context)
        if snmp_record and snmp_record.lower() == "all":
            templates_list = ENTIRE_SNMP_OID_LIST
            auto_detect_vendor = False
        elif snmp_record and snmp_record.lower().startswith("template:"):
            with open(snmp_record.lstrip("template:"), "r") as template_file:
                templates_list = template_file.readlines()
        else:
            templates_list = DEFAULT_SNMP_OID_LIST
        result = SNMPOrchestrator(snmp_parameters,
                                  auto_detect_vendor=auto_detect_vendor,
                                  template_oid_list=templates_list).create_recording() or []
        return "".join(result)

    def _new_cli_recording(self, cli_user, cli_password, cli_enable_password):
        result = ""
        return result
