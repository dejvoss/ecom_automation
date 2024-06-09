import os

from products_feed.file_generator.bol_excel_generator import BolExcelGenerator
from products_feed.products_selector import ProductsSelector, PrestaProductSelector
import settings


def create_standard_feed_by(name):
    bol_generator = BolExcelGenerator()
    big_buy_file = os.path.join(
        settings.DATA_DIR, "output_data", "bigbuy_nl_standard.csv"
    )
    selector = ProductsSelector(big_buy_file)
    products = selector.select_products_by_name(name)
    products = products[
        ["SKU", "EAN", "STOCK", "STORE_PRICE", "DELIVERY_TIME", "NAME", "DESCRIPTION"]
    ]
    for _, product in products.iterrows():
        bol_generator.add_product(product)
    bol_generator.export_feed(
        os.path.join(settings.DATA_DIR, "output_data", f"standard_feed_{name}.xlsx")
    )


def create_presta_feed(name):
    big_buy_presta_file = os.path.join(
        settings.DATA_DIR, "output_data", "bigbuy_en_prestashop.csv"
    )
    selector = PrestaProductSelector(big_buy_presta_file)
    products = selector.select_products_by_name(name)
    out_file = os.path.join(
        settings.DATA_DIR, "output_data", f"presta_feed_{name}.xlsx"
    )
    products["EAN13"] = products["EAN13"].astype(str).str.zfill(13)
    products.to_excel(out_file, index=False)
