import sys

from cloudshell.recorder.model.base_snmp_parameters import BaseSnmpParameters, config
from cloudshell.recorder.tools.snmp_tools import AUTH_PROTOCOLS, PRIV_PROTOCOLS


class SnmpV3Parameters(BaseSnmpParameters):
    def __init__(self, ip, v3_user, v3_auth_key=None, v3_priv_key=None, v3_auth_proto="NONE",
                 v3_priv_proto="NONE", port=161, is_ipv6=False, timeout=2000, retry_count=2, get_bulk_flag=False,
                 continue_on_errors=0, get_bulk_repetitions=25, v3_context_engine_id=None, v3_context=''):
        if v3_user is None:
            sys.stderr.write(
                "ERROR: --v3-user is missing\r\n")
            sys.exit(-1)
        if v3_priv_key and not v3_auth_key:
            sys.stderr.write(
                "ERROR: --v3-auth-key is missing\r\n")
            sys.exit(-1)
        if AUTH_PROTOCOLS[v3_auth_proto] == config.usmNoAuthProtocol:
            if v3_auth_key is not None:
                v3_auth_proto = 'MD5'
        else:
            if v3_auth_key is None:
                sys.stderr.write('ERROR: --v3-auth-key is missing\r\n')
                sys.exit(-1)
        if PRIV_PROTOCOLS[v3_priv_proto] == config.usmNoPrivProtocol:
            if v3_priv_key is not None:
                v3_priv_proto = 'DES'
        else:
            if v3_priv_key is None:
                sys.stderr.write('ERROR: --v3-priv-key is missing\r\n')
                sys.exit(-1)

        if v3_priv_key is None and v3_auth_key is None:
            self._sec_level = 'noAuthNoPriv'
        elif v3_priv_key is None:
            self._sec_level = 'authNoPriv'
        else:
            self._sec_level = 'authPriv'

        self._user = v3_user
        super(SnmpV3Parameters, self).__init__(ip, port, is_ipv6, timeout, retry_count, get_bulk_flag,
                                               continue_on_errors, get_bulk_repetitions, v3_context_engine_id,
                                               v3_context)
        config.addV3User(
            self._snmp_engine, v3_user,
            AUTH_PROTOCOLS[v3_auth_proto], v3_auth_key,
            PRIV_PROTOCOLS[v3_priv_proto], v3_priv_key
        )


    @property
    def get_security(self):
        return self._sec_level

    @property
    def get_user(self):
        return self._user

    @property
    def get_snmp_version(self):
        return 3
