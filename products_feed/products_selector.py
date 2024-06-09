import pandas as pd


class ProductsSelector:
    def __init__(self, products_feed):
        self.df = self.__read_all_products(products_feed)

    @staticmethod
    def __read_all_products(products_feed):
        return pd.read_csv(products_feed, sep=";", low_memory=False)

    def select_products_by_name(self, name):
        filtered_products = self.df[self.df["NAME"].str.contains(name, case=False)]
        return self._format(filtered_products)

    def select_products_by_category(self, category):
        filtered_products = self.df[
            self.df["CATEGORY"].str.contains(category, case=False)
        ]
        return self._format(filtered_products)

    def select_product_by_sku(self, sku):
        filtered_product = self.df[self.df["SKU"] == sku]
        return self._format(filtered_product)

    def _format(self, df):
        df["EAN"] = df["EAN"].astype(str).str.zfill(13)
        return df


class PrestaProductSelector(ProductsSelector):
    def _format(self, df):
        df["EAN13"] = df.loc[:, "EAN13"].astype(str).str.zfill(13)
        return df
