from utils.files_downloader.ftp_downloader import FtpDownloader


class BigBuyDownloader(FtpDownloader):
    def __init__(self, destination_dir, credentials, iso_code_language_list):
        super().__init__(destination_dir, credentials)
        self.files_lang = iso_code_language_list

    def _download_file(self, file):
        if file.split(".")[0][-2:] in self.files_lang:
            super()._download_file(file)
