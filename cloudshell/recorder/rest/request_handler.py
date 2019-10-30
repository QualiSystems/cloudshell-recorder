import os
# from functools import lru_cache
from http.server import BaseHTTPRequestHandler
# from urllib.error import HTTPError
# from urllib.parse import urlparse
import urllib3

# try:
#     from functools import lru_cache
# except ImportError:
#     from functools32 import lru_cache
#
#
# try:
#     from urllib.parse import urlparse
# except ImportError:
#     from urlparse import urlparse


class RestSimHTTPRequestHandler(BaseHTTPRequestHandler):
    URL = None
    RECORD_PATH = None
    # CASSETTE_FILE = None
    CASSETTE_NAME_TEMPLATE = "{scheme}_{host}_{port}.yaml"
    RECORD_MODE = False
    CONN_CONT_MANAGER = None
    VCR_CONT_MANAGER = None

    # @property
    # def _dst_url(self):
    #     return "{}{}".format(self.URL, self.path)

    # @property
    # @lru_cache()
    # def _dst_url_obj(self):
    #     return urlparse(self.URL)

    # @property
    # def _dst_scheme(self):
    #     return self._dst_url_obj.scheme
    #
    # @property
    # def _dst_hostname(self):
    #     return self._dst_url_obj.hostname
    #
    # @property
    # def _dst_port(self):
    #     return self._dst_url_obj.port
    #
    # def _cassette_name(self):
    #     if not self._dst_port and self._dst_scheme.lower() == 'http':
    #         port = '80'
    #     elif not self._dst_port:
    #         port = '443'
    #     else:
    #         port = self._dst_port
    #     return self.CASSETTE_NAME_TEMPLATE.format(scheme=self._dst_scheme, host=self._dst_hostname, port=port)
    #
    # @lru_cache()
    # def _cassette_path(self):
    #     if self.RECORD_PATH and os.path.isfile(self.RECORD_PATH):
    #         return self.RECORD_PATH
    #     elif self.RECORD_PATH and os.path.isdir(self.RECORD_PATH):
    #         return os.path.join(self.RECORD_PATH, self._cassette_name())
    #     else:
    #         return self._cassette_name()

    def _assign_headers(self, headers):
        for key, val in headers.items():
            self.send_header(key, val)
        self.end_headers()

    def _send_response(self, code, headers, data):
        self.send_response(code)
        self._assign_headers(headers)
        self.wfile.write(data)

    def _handle_request(self, method, handle_data=False):
        # if self.RECORD_MODE:
        #     vcr_cass_man = vcr.use_cassette(self._cassette_path(), record_mode='new_episodes',
        #                                     match_on=('method', 'path', 'query'))
        # else:
        #     vcr_cass_man = vcr.use_cassette(self._cassette_path(), match_on=('method', 'path', 'query'))
        with self.VCR_CONT_MANAGER as cass:
            if handle_data:
                content_len = int(self.headers.get('Content-Length', 0))
                data = self.rfile.read(content_len)
            else:
                data = None
            # try:
            with urllib3.connectionpool.connection_from_url(self.URL, cert_reqs='CERT_NONE') as conn:
                resp = conn.urlopen(method=method, url=self.path, headers=self.headers, body=data)
                self._send_response(resp.status, resp.headers, resp.data)
            # except HTTPError as e:
            #     self._send_response(e.code, e.headers, e.msg.encode())

    def do_GET(self):
        method = "GET"
        self._handle_request(method)

    def do_POST(self):
        method = "POST"
        self._handle_request(method, True)

    def do_PUT(self):
        method = "PUT"
        self._handle_request(method, True)

    def do_PATCH(self):
        method = "PATCH"
        self._handle_request(method, True)

    def do_DELETE(self):
        method = "DELETE"
        self._handle_request(method)
