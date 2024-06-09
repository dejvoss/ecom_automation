import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET


class PrestashopClient:
    def __init__(self, base_url, **auth_data):
        self.endpoint_url = base_url
        self.__api_key = auth_data["api_key"]
        self.__api_secret = auth_data["api_secret"]

    def auth_header(self):
        return HTTPBasicAuth(self.__api_key, self.__api_secret)


class PrestashopPoster(PrestashopClient):

    def make_post_call(self, path, xml_data):
        full_url = self.endpoint_url + path
        headers = {"Content-Type": "application/xml"}
        try:
            response = requests.post(
                full_url,
                auth=self.auth_header(),
                headers=headers,
                data=xml_data,
            )
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None


class PrestashopFilePoster(PrestashopClient):
    def make_post_call(self, path, files):
        full_url = self.endpoint_url + path
        try:
            response = requests.post(
                full_url,
                auth=self.auth_header(),
                files=files,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None


class PrestashopGetter(PrestashopClient):
    def make_get_call(self, path):
        full_url = self.endpoint_url + path + "&output_format=JSON"
        try:
            response = requests.get(
                full_url,
                auth=self.auth_header(),
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None


class PrestashopPatcher(PrestashopClient):
    def make_patch_call(self, path, xml_data):
        full_url = self.endpoint_url + path
        headers = {"Content-Type": "application/xml"}
        try:
            response = requests.patch(
                full_url,
                auth=self.auth_header(),
                headers=headers,
                data=xml_data,
            )
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None


class PrestashopDeleter(PrestashopClient):
    def make_delete_call(self, path):
        full_url = self.endpoint_url + path
        try:
            response = requests.delete(
                full_url,
                auth=self.auth_header(),
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None
