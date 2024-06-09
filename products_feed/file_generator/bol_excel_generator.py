import pandas as pd


class BolExcelGenerator:
    columns = [
        "Interne referentie",  # SKU
        "EAN",
        "Conditie",
        "Conditie commentaar",
        "Voorraad",  # Stock
        "Prijs",  # Price
        "Levertijd",  # Delivery time
        "Afleverwijze",  # Delivery method
        "Te koop",  # For sale
        "Productnaam",  # Product name
        "Beschrijving",  # Description
    ]
    from_stand_col_map = {
        "SKU": "Interne referentie",
        "EAN": "EAN",
        "STOCK": "Voorraad",
        "STORE_PRICE": "Prijs",
        "DELIVERY_TIME": "Levertijd",
        "NAME": "Productnaam",
        "DESCRIPTION": "Beschrijving",
    }

    def __init__(self):
        self.df = pd.DataFrame(columns=self.columns)

    def add_product(self, product_data: dict):
        product_df_columns = [
            "SKU",
            "EAN",
            "STOCK",
            "STORE_PRICE",
            "DELIVERY_TIME",
            "NAME",
            "DESCRIPTION",
        ]
        product_data = pd.DataFrame([product_data], columns=product_df_columns)
        product_data["Conditie"] = "Nieuw"
        product_data["DELIVERY_TIME"] = product_data["DELIVERY_TIME"].apply(
            lambda x: self.__get_delivery_time(x)
        )
        product_data["Afleverwijze"] = "verkoper"
        product_data["Te koop"] = "ja"
        product_data["Conditie commentaar"] = "Nieuw product"
        product_data.rename(columns=self.from_stand_col_map, inplace=True)
        product_data["EAN"] = product_data["EAN"].astype(str).str.zfill(13)
        self.df = pd.concat([self.df, product_data], ignore_index=True)

    def export_feed(self, output_path):
        self.df.to_excel(output_path, index=False)

    def show_feed(self):
        print(self.df)

    @staticmethod
    def __get_delivery_time(delivery_days):
        if delivery_days <= 2:
            return "1-2d"
        elif delivery_days <= 3:
            return "2-3d"
        elif delivery_days <= 5:
            return "3-5d"
        elif delivery_days <= 8:
            return "4-8d"
        else:
            return "1-8d"
