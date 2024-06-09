import os
from abc import ABC, abstractmethod


class FileDownloader(ABC):
    def __init__(self, destination_dir, **kwargs):
        self.destination_dir = destination_dir
        self.__create_dir()

    def __create_dir(self):
        if not os.path.exists(self.destination_dir):
            os.makedirs(self.destination_dir)

    @abstractmethod
    def download(self, url_or_path):
        pass
