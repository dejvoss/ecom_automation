import os

import requests

from utils.files_downloader.downloader import FileDownloader


class HttpDownloader(FileDownloader):
    def download(self, url):
        print("Downloading data from HTTP...")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to download file from {url}")
        out_file_path = os.path.join(self.destination_dir, url.split("/")[-1])
        with open(out_file_path, "wb") as file:
            file.write(response.content)
