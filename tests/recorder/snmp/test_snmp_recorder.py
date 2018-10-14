from unittest import TestCase

from mock import patch, MagicMock

from cloudshell.recorder.snmp.snmp_recorder import SnmpRecorder


# ToDo rebuild tests
class TestSnmpRecorder(TestCase):

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_create_recording(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        recorder = SnmpRecorder(params)
        oid = "1.1.1.1.1"

        # Act
        result = recorder.create_snmp_record(oid)

        # Assert
        params.snmp_engine.transportDispatcher.runDispatcher.assert_called_once()

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_create_recording_with_stop_oid(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        recorder = SnmpRecorder(params)
        oid = "1.1.1.1.1"
        stop_oid = "1.1.1.1.3"

        # Act
        result = recorder.create_snmp_record(oid, stop_oid)

        # Assert
        params.snmp_engine.transportDispatcher.runDispatcher.assert_called_once()

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_create_recording_entire_device(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        recorder = SnmpRecorder(params)
        oid = "1.1.1.1.1"

        # Act
        result = recorder.create_snmp_record(oid, get_subtree=False)

        # Assert
        params.snmp_engine.transportDispatcher.runDispatcher.assert_called_once()

    # @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    # @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    # @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    # @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    # def test_cb_fun(self, log_mock, error_mock, cmdgen_mock, udp6):
    #     # Setup
    #     params = MagicMock()
    #     snmp_engine = MagicMock()
    #     send_request_handle = MagicMock()
    #     error_indication = None
    #     error_status = None
    #     error_index = None
    #     var_bind_table = [("1", "2"), ("2", "3")]
    #     cb_ctx = MagicMock()
    #     recorder = SnmpRecorder(params)
    #     recorder._cmd_gen = MagicMock()
    #
    #     # Act
    #     recorder.cb_fun(snmp_engine, send_request_handle, error_indication,
    #                     error_status, error_index, var_bind_table, cb_ctx)
    #
    #     # Assert
    #     recorder._cmd_gen.sendVarBinds.assert_called()
    #     self.assertEqual(2, recorder._cmd_gen.sendVarBinds.call_count)
    #
    # @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    # @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    # @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    # @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    # def test_cb_fun_with_error_status(self, log_mock, error_mock, cmdgen_mock, udp6):
    #     # Setup
    #     params = MagicMock()
    #     snmp_engine = MagicMock()
    #     send_request_handle = MagicMock()
    #     error_indication = None
    #     error_status = 1
    #     error_index = None
    #     var_bind_table = MagicMock(side_effect={"1": "2", "2": "3"})
    #     cb_ctx = MagicMock()
    #     recorder = SnmpRecorder(params)
    #     recorder._cmd_gen = MagicMock()
    #
    #     # Act
    #     recorder.cb_fun(snmp_engine, send_request_handle, error_indication,
    #                     error_status, error_index, var_bind_table, cb_ctx)
    #
    #     # Assert
    #     # recorder._cmd_gen.sendVarBinds.assert_called()
    #     # self.assertEqual(2, recorder._cmd_gen.sendVarBinds.call_count)
