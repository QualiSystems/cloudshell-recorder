from unittest import TestCase

from click.testing import CliRunner
from mock import patch, Mock

from cloudshell.recorder.bootstrap import new, version


class TestBootstrap(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("cloudshell.recorder.bootstrap.RecorderOrchestrator")
    def test_new(self, record_orch_mock):
        # record_orch_mock
        result = self.runner.invoke(new, ["10.10.10.11", "--record-type", "all", "--snmp-community", "public"])

        assert result.exit_code == 0
        record_orch_mock.assert_called_once_with(u"10.10.10.11", recording_type=u"all",
                                                 destination_path=u"%APPDATA%\\Quali\\Recordings")
        record_orch_mock.return_value.create_recording.called_once_with(snmp_community="public")

    @patch("cloudshell.recorder.bootstrap.RecorderOrchestrator")
    def test_new(self, record_orch_mock):
        # record_orch_mock
        result = self.runner.invoke(new, ["10.10.10.11", "--record-type", "snmp", "--snmp-community", "public"])

        assert result.exit_code == 0
        record_orch_mock.assert_called_once_with(u"10.10.10.11", recording_type=u"all",
                                                 destination_path=u"%APPDATA%\\Quali\\Recordings")
        record_orch_mock.return_value.create_recording.called_once_with(snmp_community="public")

    @patch("cloudshell.recorder.bootstrap.RecorderOrchestrator")
    def test_new(self, record_orch_mock):
        # record_orch_mock
        result = self.runner.invoke(new, ["10.10.10.11", "--record-type", "rest",
                                          "--rest-user", "public",
                                          "--rest-password", "public"])

        assert result.exit_code == 0
        record_orch_mock.assert_called_once_with(u"10.10.10.11", recording_type=u"rest",
                                                 destination_path=u"%APPDATA%\\Quali\\Recordings")
        record_orch_mock.return_value.create_recording.called_once_with(rest_user="public", rest_password="public")

    @patch("cloudshell.recorder.bootstrap.RecorderOrchestrator")
    def test_new(self, record_orch_mock):
        # record_orch_mock
        result = self.runner.invoke(new, ["10.10.10.11", "--record-type", "cli",
                                          "--cli-user", "public",
                                          "--cli-password", "public"])

        assert result.exit_code == 0
        record_orch_mock.assert_called_once_with(u"10.10.10.11", recording_type=u"cli",
                                                 destination_path=u"%APPDATA%\\Quali\\Recordings")
        record_orch_mock.return_value.create_recording.called_once_with(cli_user="public", cli_password="public")

    @patch("cloudshell.recorder.bootstrap.RecorderOrchestrator")
    def test_new(self, record_orch_mock):
        error_msg = "something wrong"
        record_orch_mock.side_effect = Exception(error_msg)
        result = self.runner.invoke(new, ["10.10.10.11", "--record-type", "all", "--snmp-community", "public"])

        assert result.exit_code == -1
        assert "ERROR: {}".format(error_msg) in result.output

    @patch("cloudshell.recorder.bootstrap.pkg_resources")
    def test_version(self, pkg_mock):
        # Setup
        obj = Mock()
        obj.version = "correct_version"
        pkg_mock.get_distribution = Mock(return_value=obj)

        # Act
        result = self.runner.invoke(version)

        # Assert
        assert result.exit_code == 0
        assert result.output == "cloudshell-recorder version correct_version\n"
