from unittest import TestCase

from click.testing import CliRunner

from cloudshell.recorder.bootstrap import new, version


class TestBootstrap(TestCase):
    def test_new(self):
        result = CliRunner().invoke(new, ['1.1.1.1', '--snmp-community=public', '--record-type=snmp'])
        self.assertEqual(0, result.exit_code)

    def test_version(self):
        result = CliRunner().invoke(version)
        self.assertEqual(1, result.exit_code)
