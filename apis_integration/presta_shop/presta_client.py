from requests.auth import HTTPBasicAuth


class PrestashopClient:
    def __init__(self, base_url, **auth_data):
        self.endpoint_url = base_url
        self.__api_key = auth_data["api_key"]
        self.__api_secret = auth_data["api_secret"]

    def get_auth_header(self):
        return HTTPBasicAuth(self.__api_key, self.__api_secret)
