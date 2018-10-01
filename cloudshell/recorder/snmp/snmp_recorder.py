import time
import sys

import traceback
from pyasn1.type import univ
from pysnmp.proto import rfc1902
from pysnmp.proto import rfc1905

from cloudshell.recorder.model.snmp_record import SnmpRecord

try:
    from pysnmp.carrier.asynsock.dgram import udp6
except ImportError:
    udp6 = None
from pysnmp.entity.rfc3413 import cmdgen
from snmpsim import error, log


class SnmpRecorder(object):
    def __init__(self, snmp_parameters):
        self.snmp_parameters = snmp_parameters
        self.output_file = list()
        self.data_file_handler = SnmpRecord()
        self.__oid = None
        self.__stop_oid = None
        self._cmd_gen = None

    def create_snmp_record(self, oid, get_subtree=True):
        self.__oid = univ.ObjectIdentifier(oid)
        if get_subtree:
            _stop_oid = "{}{}".format(oid[:-1], int(oid[-1:]) + 1)
            self.__stop_oid = univ.ObjectIdentifier(_stop_oid)

        cbCtx = {
            'total': 0,
            'count': 0,
            'errors': 0,
            'iteration': 0,
            'reqTime': time.time(),
            '': True,
            'retries': self.snmp_parameters.continue_on_errors,
            'lastOID': oid
        }

        if self.snmp_parameters.get_bulk_flag:
            self._cmd_gen = cmdgen.BulkCommandGenerator()

            self._cmd_gen.sendVarBinds(
                self.snmp_parameters.snmp_engine,
                'tgt',
                self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                0, self.snmp_parameters.get_bulk_repetitions,
                [(self.__oid, None)],
                self.cbFun, cbCtx
            )
        else:
            self._cmd_gen = cmdgen.NextCommandGenerator()

            self._cmd_gen.sendVarBinds(
                self.snmp_parameters.snmp_engine,
                'tgt',
                self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                [(self.__oid, None)],
                self.cbFun, cbCtx
            )

        log.msg('Sending initial %s request for %s ....' % (
            self.snmp_parameters.get_bulk_flag and 'GETBULK' or 'GETNEXT', self.__oid))

        t = time.time()

        # Python 2.4 does not support the "finally" clause

        exc_info = None

        try:
            self.snmp_parameters.snmp_engine.transportDispatcher.runDispatcher()
        except KeyboardInterrupt:
            log.msg('Shutting down process...')
        except Exception:
            exc_info = sys.exc_info()

        # self.snmp_parameters.snmp_engine.transportDispatcher.closeDispatcher()

        t = time.time() - t

        cbCtx['total'] += cbCtx['count']

        log.msg('OIDs dumped: %s, elapsed: %.2f sec, rate: %.2f OIDs/sec, errors: %d' % (
            cbCtx['total'], t, t and cbCtx['count'] // t or 0, cbCtx['errors']))

        if exc_info:
            for line in traceback.format_exception(*exc_info):
                log.msg(line.replace('\n', ';'))

        return self.output_file

    def cbFun(self, snmpEngine, sendRequestHandle, errorIndication,
              errorStatus, errorIndex, varBindTable, cbCtx):
        if errorIndication and not cbCtx['retries']:
            cbCtx['errors'] += 1
            log.msg('SNMP Engine error: %s' % errorIndication)
            return
        # SNMPv1 response may contain noSuchName error *and* SNMPv2c exception,
        # so we ignore noSuchName error here
        if errorStatus and errorStatus != 2 or errorIndication:
            log.msg('Remote SNMP error %s' % (errorIndication or errorStatus.prettyPrint()))
            if cbCtx['retries']:
                try:
                    nextOID = varBindTable[-1][0][0]
                except IndexError:
                    nextOID = cbCtx['lastOID']
                else:
                    log.msg('Failed OID: %s' % nextOID)
                # fuzzy logic of walking a broken OID
                if len(nextOID) < 4:
                    pass
                elif (self.snmp_parameters.continue_on_errors - cbCtx[
                    'retries']) * 10 / self.snmp_parameters.continue_on_errors > 5:
                    nextOID = nextOID[:-2] + (nextOID[-2] + 1,)
                elif nextOID[-1]:
                    nextOID = nextOID[:-1] + (nextOID[-1] + 1,)
                else:
                    nextOID = nextOID[:-2] + (nextOID[-2] + 1, 0)

                cbCtx['retries'] -= 1
                cbCtx['lastOID'] = nextOID

                log.msg('Retrying with OID %s (%s retries left)...' % (nextOID, cbCtx['retries']))

                # initiate another SNMP walk iteration
                if self.snmp_parameters.get_bulk_flag:
                    self._cmd_gen.sendVarBinds(
                        snmpEngine,
                        'tgt',
                        self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                        0, self.snmp_parameters.get_bulk_repetitions,
                        [(nextOID, None)],
                        self.cbFun, cbCtx
                    )
                else:
                    self._cmd_gen.sendVarBinds(
                        snmpEngine,
                        'tgt',
                        self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                        [(nextOID, None)],
                        self.cbFun, cbCtx
                    )

            cbCtx['errors'] += 1

            return

        if self.snmp_parameters.continue_on_errors != cbCtx['retries']:
            cbCtx['retries'] += 1

        if varBindTable and varBindTable[-1] and varBindTable[-1][0]:
            cbCtx['lastOID'] = varBindTable[-1][0][0]

        stopFlag = False

        # Walk var-binds
        for varBindRow in varBindTable:
            for oid, value in varBindRow:
                # EOM
                if self.__stop_oid and oid >= self.__stop_oid:
                    stopFlag = True
                if (value is None or
                        value.tagSet in (rfc1905.NoSuchObject.tagSet,
                                         rfc1905.NoSuchInstance.tagSet,
                                         rfc1905.EndOfMibView.tagSet)):
                    stopFlag = True

                # remove value enumeration
                if value.tagSet == rfc1902.Integer32.tagSet:
                    value = rfc1902.Integer32(value)

                if value.tagSet == rfc1902.Unsigned32.tagSet:
                    value = rfc1902.Unsigned32(value)

                if value.tagSet == rfc1902.Bits.tagSet:
                    value = rfc1902.OctetString(value)

                # Build .snmprec record

                context = {
                    'origOid': oid,
                    'origValue': value,
                    'count': cbCtx['count'],
                    'total': cbCtx['total'],
                    'iteration': cbCtx['iteration'],
                    'reqTime': cbCtx['reqTime'],
                    'startOID': self.__oid,
                    'stopFlag': stopFlag,
                }

                try:
                    line = self.data_file_handler.format(oid, value, **context).replace("|", ", ")
                except error.MoreDataNotification:
                    cbCtx['count'] = 0
                    cbCtx['iteration'] += 1

                    moreDataNotification = sys.exc_info()[1]
                    if 'period' in moreDataNotification:
                        log.msg(
                            '%s OIDs dumped, waiting %.2f sec(s)...' % (
                                cbCtx['total'], moreDataNotification['period']))
                        time.sleep(moreDataNotification['period'])

                    # initiate another SNMP walk iteration
                    if self.snmp_parameters.get_bulk_flag:
                        self._cmd_gen.sendVarBinds(
                            snmpEngine,
                            'tgt',
                            self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                            0, self.snmp_parameters.get_bulk_repetitions,
                            [(self.__oid, None)],
                            self.cbFun, cbCtx
                        )
                    else:
                        self._cmd_gen.sendVarBinds(
                            snmpEngine,
                            'tgt',
                            self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                            [(self.__oid, None)],
                            self.cbFun, cbCtx
                        )

                    stopFlag = True  # stop current iteration

                except error.NoDataNotification:
                    pass
                except error.SnmpsimError:
                    log.msg('ERROR: %s' % (sys.exc_info()[1],))
                    continue
                else:
                    self.output_file.append(line)

                    cbCtx['count'] += 1
                    cbCtx['total'] += 1

                    if cbCtx['count'] % 100 == 0:
                        log.msg('OIDs dumped: %s/%s' % (
                            cbCtx['iteration'], cbCtx['count']))

        # Next request time
        cbCtx['reqTime'] = time.time()
        # Continue walking
        return not stopFlag
