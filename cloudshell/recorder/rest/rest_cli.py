import logging
import os
import ssl
import sys
import urllib
from http.server import HTTPServer
from urllib.parse import urlparse

import click
import pkg_resources
import urllib3
import vcr

from cloudshell.recorder.rest.request_handler import RestSimHTTPRequestHandler

urllib3.disable_warnings()

CASSETTE_NAME_TEMPLATE = "{scheme}_{host}_{port}.yaml"
MATCH_ON = ('method', 'path', 'query')


def _enable_debug():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s]: %(name)s %(module)s - %(funcName)-20s %(message)s")


@click.group(invoke_without_command=True)
@click.option(u'--version', u'-v', is_flag=True, default=False, help='Package version.')
@click.pass_context
def rest_cli(ctx, version):
    """For more information on a specific command, type migration_tool COMMAND --help"""
    if version:
        version = pkg_resources.get_distribution("cloudshell-recording").version
        click.echo('Version: {}'.format(version))
        ctx.exit(0)
    else:
        if not ctx.invoked_subcommand:
            click.echo(ctx.get_help())


@rest_cli.command()
@click.option("--host", "-h", default="localhost",
              help="Listen host. Default: localhost")
@click.option("--port", "-p", default=None,
              help="Listen port. Default: dst url port")
@click.option("--scheme", "-s", default=None, help="Listen scheme, http or https, Default: dst url scheme.")
@click.option("--file-path", "-f", default=None, help="Record path. Default: current path.")
@click.option("--debug", "-d", is_flag=True, default=False, help="Enable debug.")
@click.option("--record", "-r", "record_mode", is_flag=True, default=False, help="Enable record mode.")
@click.argument(u'url', type=str, default=None, required=True)
def record(host, port, scheme, file_path, debug, record_mode, url):
    if debug:
        _enable_debug()

    RestSimHTTPRequestHandler.URL = url
    RestSimHTTPRequestHandler.RECORD_PATH = file_path
    RestSimHTTPRequestHandler.RECORD_MODE = False

    if record_mode:
        vcr_cass_man = vcr.use_cassette(_cassette_path(url, file_path), record_mode='new_episodes',
                                        match_on=MATCH_ON)
    else:
        vcr_cass_man = vcr.use_cassette(_cassette_path(url, file_path), match_on=MATCH_ON)

    RestSimHTTPRequestHandler.VCR_CONT_MANAGER = vcr_cass_man

    url_obj = urllib.parse.urlparse(url)
    if not port and not url_obj.port:
        if scheme == "http" or url_obj.scheme == "http":
            port = 80
        else:
            port = 443
    else:
        port = port or url_obj.port
    server = HTTPServer((host, port), RestSimHTTPRequestHandler)
    if (scheme and scheme == "https") or url_obj.scheme == "https":
        server.socket = ssl.wrap_socket(server.socket, server_side=True,
                                        certfile=os.path.join(os.path.dirname(__file__), 'default.pem'))
    server.serve_forever()


def _cassette_name(url):
    url_obj = urllib.parse.urlparse(url)
    if not url_obj.port and url_obj.scheme.lower() == 'http':
        port = '80'
    elif not url_obj.port:
        port = '443'
    else:
        port = url_obj.port
    return CASSETTE_NAME_TEMPLATE.format(scheme=url_obj.scheme, host=url_obj.hostname, port=port)


def _cassette_path(url, path):
    if path and os.path.isfile(path):
        return path
    elif path and os.path.isdir(path):
        return os.path.join(path, _cassette_name(url))
    else:
        return _cassette_name(url)


@rest_cli.command()
def simulate():
    pass


if __name__ == '__main__':
    rest_cli()
