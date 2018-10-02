import click
import pkg_resources

# from shellfoundry.decorators import shellfoundry_version_check
# from shellfoundry.commands.dist_command import DistCommandExecutor
# from shellfoundry.commands.generate_command import GenerateCommandExecutor
# from shellfoundry.commands.install_command import InstallCommandExecutor
# from shellfoundry.commands.list_command import ListCommandExecutor
# from shellfoundry.commands.new_command import NewCommandExecutor
# from shellfoundry.commands.extend_command import ExtendCommandExecutor
# from shellfoundry.commands.pack_command import PackCommandExecutor
# from shellfoundry.commands.config_command import ConfigCommandExecutor
# from shellfoundry.commands.show_command import ShowCommandExecutor
# from shellfoundry.utilities import GEN_ONE, GEN_TWO, LAYER_ONE, NO_FILTER
from cloudshell.recorder.recorder_orchestrator import RecorderOrchestrator


# from cloudshell.recorder.tools.bootstrap_tools import CLI, SNMP, NO_FILTER


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Displays the cloudshell-device-recorder version
    """
    click.echo(
        u'cloudshell-device-recorder version ' + pkg_resources.get_distribution(u'cloudshell-device-recorder').version)


@cli.command()
@click.argument(u'ip')
@click.option(u'--snmp-community')
@click.option(u'--snmp-user')
@click.option(u'--snmp-password')
@click.option(u'--snmp-private-key')
@click.option(u'--snmp-auth-protocol', default="NONE")
@click.option(u'--snmp-priv-protocol', default="NONE")
@click.option(u'--snmp-auto-detect-vendor', default="true")
@click.option(u'--snmp-record', default="shells_based",
              help="Specify an oid template file for record adding 'template:'PATH_TO_FILE''. "
                   "Or set it to 'all' to record entire device. "
                   "Default value is 'shells_based', and will record all oids used by the Shells.")
@click.option(u'--destination-path', default="%APPDATA%\\Quali\\Recordings")
@click.option(u'--snmp-timeout', default=2000)
@click.option(u'--snmp-retries', default=2)
@click.option(u'--snmp-bulk', default="false")
@click.option(u'--snmp-bulk-repetitions', default=25)
def new(ip,
        destination_path,
        cli_user=None,
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
        snmp_auto_detect_vendor=None):
    """
    Creates a new device recording based on a template
    """
    RecorderOrchestrator(ip, recording_type="both", destination_path=destination_path).new_recording(
        cli_user=cli_user, cli_password=cli_password,
        cli_enable_password=cli_enable_password,
        snmp_community=snmp_community,
        snmp_user=snmp_user, snmp_password=snmp_password,
        snmp_private_key=snmp_private_key,
        snmp_auth_protocol=snmp_auth_protocol,
        snmp_priv_protocol=snmp_priv_protocol,
        snmp_record=snmp_record,
        snmp_timeout=snmp_timeout,
        snmp_bulk=snmp_bulk,
        snmp_retries=snmp_retries,
        snmp_bulk_repetitions=snmp_bulk_repetitions,
        snmp_auto_detect_vendor=snmp_auto_detect_vendor)
