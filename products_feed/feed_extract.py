import os
import pandas as pd

import settings
from products_feed import feed_update

STANDARD_VIDA_EXTRACT_FILE_PATH = os.path.join(
    settings.DATA_DIR, "output_data", "vida_feed.csv"
)
STANDARD_BIG_BUY_EXTRACT_FILE_PATH = os.path.join(
    settings.DATA_DIR, "output_data", "bigbuy_nl_standard.csv"
)


def extract_feeds():
    extract_vida_feed()
    extract_big_buy_feed()


def extract_vida_feed():
    vida_extract_timestamp = os.path.getmtime(
        os.path.join(STANDARD_VIDA_EXTRACT_FILE_PATH)
    )
    if (
        feed_update.get_last_feed_update(settings.VIDA_FEED_DIR)
        < vida_extract_timestamp
    ):
        return
    print("Extracting vida feed")
    vida_file = os.path.join(
        settings.VIDA_FEED_DIR, os.listdir(settings.VIDA_FEED_DIR)[0]
    )
    vida_df = pd.read_csv(vida_file, sep=",", low_memory=False, dtype={"EAN": str})
    vida_df = vida_df[vida_df["B2B price"] > 0]
    vida_df.rename(columns=settings.VIDA_COL_NAMES_MAP, inplace=True)
    vida_df.columns = vida_df.columns.str.upper()
    vida_df.columns = vida_df.columns.str.replace(" ", "")
    vida_df.to_csv(
        os.path.join(settings.DATA_DIR, "output_data", "vida_feed.csv"),
        index=False,
        sep=";",
    )


def extract_big_buy_feed():
    big_buy_extract_timestamp = os.path.getmtime(
        os.path.join(STANDARD_BIG_BUY_EXTRACT_FILE_PATH)
    )
    if (
        feed_update.get_last_feed_update(settings.BIG_BUY_FEED_DIR)
        < big_buy_extract_timestamp
    ):
        return
    for language in settings.BIG_BUY_LANGUAGES:
        print(f"Extracting big buy feeds for {language}")
        extract_standard_bb_feed(language)
        extract_prestashop_bb_feed(language)


def extract_standard_bb_feed(language):
    files_dir = os.path.join(
        settings.BIG_BUY_FEED_DIR, "files", "products", "csv", "standard"
    )
    extracted_df = combine_csv_files(files_dir, language)
    if extracted_df is not None:
        extracted_df.rename(columns=settings.BB_STANDARD_COL_NAMES_MAP, inplace=True)
        extracted_df = extracted_df[extracted_df["CONDITION"] == "NEW"]
        extracted_df["DELIVERY_TIME"] = 5
        extracted_df.to_csv(
            os.path.join(
                settings.DATA_DIR, "output_data", f"bigbuy_{language}_standard.csv"
            ),
            index=False,
            sep=";",
        )


def extract_prestashop_bb_feed(language):
    files_dir = os.path.join(
        settings.BIG_BUY_FEED_DIR, "files", "products", "csv", "prestashop"
    )
    extracted_df = combine_csv_files(files_dir, language)
    if extracted_df is not None:
        extracted_df.to_csv(
            os.path.join(
                settings.DATA_DIR, "output_data", f"bigbuy_{language}_prestashop.csv"
            ),
            index=False,
            sep=";",
        )


def combine_csv_files(files_dir, file_filter):
    files = [f for f in os.listdir(files_dir) if file_filter in f]
    if not files:
        return

    final_df = pd.DataFrame()
    for file in files:
        if file.endswith(".csv") and file_filter in file:
            f_path = os.path.join(files_dir, file)
            df = pd.read_csv(f_path, sep=";", low_memory=False, dtype={"EAN13": str})
            if df.shape[0] > 0:
                final_df = pd.concat([final_df, df], ignore_index=True)

    return final_df
