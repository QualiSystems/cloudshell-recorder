class RestSession(object):
    def __init__(self, username=None, password=None, token=None, headers=None):
        self.username = username
        self.password = password
        self.token = token
        self.headers = headers


class RestRequest(object):
    def __init__(self, uri, method='GET', data=None, headers=None):
        self.method = method
        self.uri = uri
        self.data = data
        self.headers = headers

    def __hash__(self):
        return hash(self.method) | hash(self.uri) | hash(self.data)

    def __eq__(self, other):
        """
        :param RestRequest other:
        """
        return self.uri == other.uri and self.method == other.method and self.data == other.data


class RestResponse(object):
    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self.content = content
