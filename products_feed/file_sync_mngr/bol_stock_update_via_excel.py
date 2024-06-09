import settings
import os
import pandas as pd
from datetime import datetime


def create_bol_stock_file():
    bol_stock = read_bol_excel_bestand()
    vida_feed = read_vida_feed()
    big_buy_feed = read_big_buy_feed()
    feed = pd.concat([vida_feed, big_buy_feed], ignore_index=True)
    feed.rename(columns={"STOCK": "STOCK_FEEDS"}, inplace=True)
    bol_stock = bol_stock.merge(feed, on="EAN", how="left")
    bol_stock["STOCK"] = bol_stock["STOCK"].fillna(0, inplace=True)
    bol_stock.to_excel(
        os.path.join(settings.DATA_DIR, "output_data", "bol_stock", "bol_stock.xlsx"),
        index=False,
    )
    print("\nBol stock file created successfully.\n".center(80))


def read_vida_feed():
    print("Reading vida feed...")
    vida_feed = os.path.join(settings.DATA_DIR, "output_data", "vida_feed.csv")
    return pd.read_csv(vida_feed, sep=";", dtype={"EAN": str}, usecols=["EAN", "STOCK"])


def read_big_buy_feed():
    print("Reading big buy feed...")
    bol_feed = os.path.join(settings.DATA_DIR, "output_data", "bigbuy_nl_standard.csv")
    return pd.read_csv(bol_feed, sep=";", dtype={"EAN": str}, usecols=["EAN", "STOCK"])


def read_bol_excel_bestand():
    print("Reading bol excel bestand...")
    bol_excel_bestand_dir = os.path.join(
        settings.DATA_DIR, "input_data", "bol_excel_aanbod"
    )
    bol_excel_bestand = max(
        [
            os.path.join(bol_excel_bestand_dir, f)
            for f in os.listdir(bol_excel_bestand_dir)
        ],
        key=os.path.getctime,
    )
    if (
        datetime.fromtimestamp(os.path.getctime(bol_excel_bestand)).date()
        < datetime.now().date()
    ):
        raise ValueError("Bol excel bestand is not up to date")
    return pd.read_excel(
        bol_excel_bestand,
        dtype={"EAN": str},
        skiprows=[0, 1],
        sheet_name="bol.com artikelimport hulp v2.3",
    )
