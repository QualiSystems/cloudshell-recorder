import requests
import yaml

from cloudshell.recorder.rest.model import RestResponse


class RestRecorder(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.record_table = {}

    def initialize(self, session_model):
        """
        :param cloudshell.recorder.rest.model.RestSession session_model:
        :return:
        """
        self.session.auth = (session_model.username, session_model.password)
        self.session.verify = False

    def _build_url(self, uri):
        return self.base_url + uri

    def record(self, requests_table):
        """
        :param list[cloudshell.recorder.rest.model.RestRequest] requests_table:
        :return:
        """
        for request in requests_table:
            resp = self.session.request(method=request.method, url=self._build_url(request.uri), data=request.data,
                                        headers=request.headers)
            self.record_table[request] = RestResponse(resp.status_code, dict(resp.headers), resp.text)

    def save(self, path):
        with open(path, "w") as file_descr:
            data = yaml.dump(self.record_table, default_flow_style=False, allow_unicode=True, encoding=None)
            file_descr.write(data)
