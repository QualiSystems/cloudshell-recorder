import os
from functools import lru_cache

import yaml

from cloudshell.recorder.rest.model import RestRequest, RestSession


class Configuration(object):
    SESSION_KEY = 'Session'
    RECORDS_KEY = 'Requests'

    def __init__(self, config_path):
        self._config_path = config_path

    @property
    @lru_cache()
    def _config(self):
        with open(self._config_path, 'r') as config:
            return yaml.load(config)

    def get_session(self):
        return RestSession(**self._config.get(self.SESSION_KEY))

    def get_requests(self):
        table = []
        for record_args in self._config.get(self.RECORDS_KEY):
            table.append(RestRequest(**record_args))
        return table
