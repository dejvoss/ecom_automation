import ftplib
import os

from utils.files_downloader.downloader import FileDownloader


class FtpDownloader(FileDownloader):
    def __init__(self, destination_dir, credentials):
        super().__init__(destination_dir)
        self.__host = credentials["host"]
        self.__user = credentials["user"]
        self.__pass = credentials["pass"]
        self.__ftp = None

    def download(self, ftp_file_path):
        print("Downloading data from FTP...")
        self.__connect()
        if self.__is_folder(ftp_file_path):
            self.__download_folder(ftp_file_path)
        else:
            self._download_file(ftp_file_path)
        self.__ftp.quit()

    def __connect(self):
        self.__ftp = ftplib.FTP(self.__host)
        self.__ftp.login(self.__user, self.__pass)

    def __is_folder(self, path):
        current_dir = self.__ftp.pwd()
        try:
            self.__ftp.cwd(path)
        except ftplib.error_perm:
            return False
        else:
            self.__ftp.cwd(current_dir)
            return True

    def _download_file(self, file):
        ftp_dir = self.__ftp.pwd()
        ftp_dir = ftp_dir[1:] if ftp_dir[0] == "/" else ftp_dir
        if ftp_dir not in file:
            destination_file_path = os.path.join(
                self.destination_dir, ftp_dir.replace("/", "\\"), file
            )
        else:
            destination_file_path = os.path.join(
                self.destination_dir, file.replace("/", "\\")
            )
        if not os.path.exists(os.path.dirname(destination_file_path)):
            os.makedirs(os.path.dirname(destination_file_path))
        with open(destination_file_path, "wb") as f:
            try:
                self.__ftp.retrbinary("RETR " + file, f.write)
            except ftplib.error_perm:
                print(f"Failed to download {file}")

    def __download_folder(self, folder_path):
        self.__ftp.cwd(folder_path)
        objects = self.__ftp.nlst()
        for obj in objects:
            if self.__is_folder(obj):
                self.__download_folder(obj)
                self.__ftp.cwd("..")
            else:
                self._download_file(obj)
