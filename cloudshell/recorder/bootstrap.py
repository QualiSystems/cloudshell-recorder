import click
import pkg_resources

from cloudshell.recorder.recorder_orchestrator import RecorderOrchestrator


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Displays the cloudshell-recorder version
    """

    click.echo(
        u'cloudshell-recorder version ' + pkg_resources.get_distribution('cloudshell-recorder').version)


@cli.command()
@click.argument(u'ip')
@click.option(u'--snmp-community', help="Snmp v1 or v2 community")
@click.option(u'--snmp-user', help="Snmp v3 user")
@click.option(u'--snmp-password', help="Snmp password or auth")
@click.option(u'--snmp-private-key', help="Snmp privacy key")
@click.option(u'--snmp-auth-protocol', default="NONE",
              help="Snmp auth encryption type: SHA, MD5, SHA224, SHA256, SHA384, SHA512, NONE. Default is NONE.")
@click.option(u'--snmp-priv-protocol', default="NONE",
              help="Snmp privacy encryption type: DES, 3DES, AES, AES128, AES192, AES192BLMT, AES256, AES256BLMT, "
                   "NONE. Default is NONE.")
@click.option(u'--snmp-auto-detect-vendor', is_flag=True, help="Enables auto detect of device manufacturer")
@click.option(u'--snmp-record', default="shells_based",
              help="Specify an oid template file for record adding 'template:PATH_TO_FILE'. "
                   "Or set it to 'all' to record entire device. "
                   "Default value is 'shells_based', and will record all oids used by the Shells.")
@click.option(u'--destination-path', default="%APPDATA%\\Quali\\Recordings",
              help="Destination path, i.e. %APPDATA%\\Quali\\Recordings")
@click.option(u'--snmp-timeout', default=2000, help="Snmp timeout")
@click.option(u'--snmp-retries', default=2, help="Amount of snmp retires")
@click.option(u'--snmp-bulk', is_flag=True, help="Add to use snmpbulk for better performance")
@click.option(u'--snmp-bulk-repetitions', default=25, help="Amount of snmpbulk repetitions")
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
        snmp_bulk=False,
        snmp_bulk_repetitions=25,
        snmp_auto_detect_vendor=False):
    """
    Creates a new device recording based on a template
    """
    if not snmp_user or not snmp_community:
        with click.Context(new) as context:
            click.echo(new.get_help(context))
            return

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
