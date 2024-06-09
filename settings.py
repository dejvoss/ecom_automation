import os
from dotenv import load_dotenv

TEST_MODE = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# add to path to import from other directories
DATA_DIR = os.path.join(BASE_DIR, "data_files")

load_dotenv(os.path.join(BASE_DIR, ".env"))

PROD_MEDIA_DIR = r"C:\Users\DeOs\Pictures\ecom\autoproducts"


# DROP-SHIPPING PARTNERS
# BIG_BUY
if TEST_MODE:
    BIG_BUY_API_KEY = os.environ.get("BIG_BUY_API_KEY_TEST")
    BIG_BUY_API_URL = "https://api.sandbox.bigbuy.eu/"
else:
    BIG_BUY_API_KEY = os.environ.get("BIG_BUY_API_KEY")
    BIG_BUY_API_URL = "https://api.bigbuy.eu/"

BIG_BUY_FEED_DIR = os.path.join(DATA_DIR, "big_buy")
BIG_BUY_FTP_HOST = os.environ.get("BIG_BUY_FTP_HOST")
BIG_BUY_FTP_USER = os.environ.get("BIG_BUY_FTP_USER")
BIG_BUY_FTP_PASS = os.environ.get("BIG_BUY_FTP_PASS")
BIG_BUY_LANGUAGES = ["en", "pl", "nl"]
BIG_BUY_FEED_UPDATE_INTERVAL = 24  # hours
BIG_BUY_FEED_EARLIEST_HOUR = 12
BB_STANDARD_COL_NAMES_MAP = {
    "ID": "SKU",
    "CATEGORY": "CATEGORY_ID",
    "PRICE": "STORE_PRICE",
    "PVD": "B2B_PRICE",
    "EAN13": "EAN",
}

# VIDA
VIDA_FEED_DIR = os.path.join(DATA_DIR, "vidaxl")
VIDA_CSV_FEED_URL = os.environ.get("VIDA_CSV_FEED_URL")
VIDA_FEED_UPDATE_INTERVAL = 1  # hours
VIDA_COL_NAMES_MAP = {
    "Title": "NAME",
    "vidaXL Price": "STORE_PRICE",
    "Webshop price": "WEBSHOP_PRICE",
    "estimated_total_delivery_time": "DELIVERY_TIME",
}

# MAIN E-COMMERCE PLATFORM
# PRESTASHOP
PRESTASHOP_API_URL = os.environ.get("STORE_API_URL")
PRESTASHOP_API_TOKEN = os.environ.get("STORE_API_KEY")
PRESTASHOP_API_SECRET = os.environ.get("STORE_API_SECRET")

IMG_FILE_ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "gif")
