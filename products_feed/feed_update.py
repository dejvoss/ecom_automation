import os
from datetime import datetime

from utils.files_downloader.http_downloader import HttpDownloader
from products_feed.big_buy_downloader import BigBuyDownloader
import settings


def update_feeds():
    update_vida_feed()
    update_big_buy_feed()


def update_vida_feed():
    last_vida_feed_update = get_last_feed_update(settings.VIDA_FEED_DIR)
    if is_feed_outdated(last_vida_feed_update, settings.VIDA_FEED_UPDATE_INTERVAL):
        print("Updating vida feed")
        downloader = HttpDownloader(settings.VIDA_FEED_DIR)
        downloader.download(settings.VIDA_CSV_FEED_URL)


def update_big_buy_feed():
    if datetime.now().hour < settings.BIG_BUY_FEED_EARLIEST_HOUR:
        return
    bb_feed_last_update = get_last_feed_update(settings.BIG_BUY_FEED_DIR)
    if is_feed_outdated(bb_feed_last_update, settings.BIG_BUY_FEED_UPDATE_INTERVAL):
        print("Updating big buy feed")
        bb_ftp_credentials = get_big_buy_credentials()
        downloader = BigBuyDownloader(
            settings.BIG_BUY_FEED_DIR, bb_ftp_credentials, settings.BIG_BUY_LANGUAGES
        )
        downloader.download("files")


def get_last_feed_update(feed_path):
    if not os.listdir(feed_path):
        return 0
    feed_file = os.path.join(feed_path, os.listdir(feed_path)[0])
    if os.path.exists(feed_file):
        if os.path.isfile(feed_file):
            return os.path.getmtime(feed_file)
        else:
            return get_last_feed_update(feed_file)
    else:
        return 0


def is_feed_outdated(feed_last_update, feed_interval):
    return feed_last_update + feed_interval * 3600 < datetime.now().timestamp()


def get_big_buy_credentials():
    return {
        "host": settings.BIG_BUY_FTP_HOST,
        "user": settings.BIG_BUY_FTP_USER,
        "pass": settings.BIG_BUY_FTP_PASS,
    }
