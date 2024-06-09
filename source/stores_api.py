import requests
import os
import pandas as pd
from datetime import datetime, timedelta


if __name__ == "__main__":
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from source.gpt_generator import ProductDescriptionGenerator


class VidaAPI:
    feed_path = os.path.join(settings.DATA_DIR, "vida_feed.parquet")
    feed_update_date = (
        datetime.fromtimestamp(os.path.getmtime(feed_path))
        if os.path.exists(feed_path)
        else None
    )

    def __init__(self):
        self.__auth_data = (
            os.environ.get("VIDA_API_LOGIN"),
            os.environ.get("VIDA_API_KEY"),
        )
        self.__base_url = "https://b2b.vidaxl.com/api_customer"
        self.__feed_url = "http://transport.productsup.io/cf7871c3eb59dc3fd0e5/channel/188055/vidaXL_nl_dropshipping.csv"
        self.product_source = "feed"

    def __str__(self):
        return f"VidaXL using data_files from: {self.product_source}"

    def change_source(self):
        if self.product_source == "feed":
            self.product_source = "api"
        else:
            self.product_source = "feed"

    def get_available_products(self):
        if self.product_source == "feed":
            return self.__get_avail_products_feed()
        else:
            return self.__get_avail_products_api()

    def get_category_products(self, category):
        if self.product_source == "feed":
            return self.__get_cat_products_feed(category)
        else:
            return self.__get_cat_products_api(category)

    def get_specific_product(self, sku):
        if self.product_source == "feed":
            return self.__get_specific_product_feed(sku)
        else:
            return self.__get_specific_product_api(sku)

    def __number_of_products(self):
        response = requests.get(
            f"{self.__base_url}/products?limit=10", auth=self.__auth_data
        )
        if response.status_code == 200:
            return response.json()["pagination"]["total"]

    def __get_avail_products_api(self):
        # get all products from vida (limit to 500)
        # authenticate via simple http auth
        available_products = []
        total_products = self.__number_of_products()
        for i in range(0, 500, total_products):
            response = requests.get(
                f"{self.__base_url}/products?limit=10&offset={i}", auth=self.__auth_data
            )
            if response.status_code == 200:
                for product in response.json()["data_files"]:
                    if product["quantity"] > 0:
                        available_products.append(product)
        return available_products

    def __get_avail_products_feed(self):
        if (
            VidaAPI.feed_update_date is None
            or datetime.now() - VidaAPI.feed_update_date > timedelta(hours=1)
        ):
            self.__update_feed()
        data = pd.read_parquet(VidaAPI.feed_path)
        data = data[data["B2B price"] > 0]
        return data[data["Stock"] > 0]

    def __get_specific_product_api(self, sku):
        response = requests.get(
            f"{self.__base_url}/products?code_eq={sku}", auth=self.__auth_data
        )
        if response.status_code == 200:
            return response.json()[0]

    def __get_specific_product_feed(self, sku):
        if (
            VidaAPI.feed_update_date is None
            or datetime.now() - VidaAPI.feed_update_date > timedelta(hours=1)
        ):
            self.__update_feed()
        data = pd.read_parquet(VidaAPI.feed_path)
        return data[data["SKU"] == sku]

    def __update_feed(self):
        data = pd.read_csv(self.__feed_url, sep=",", low_memory=False)
        data.to_parquet(self.feed_path)
        data.to_csv(os.path.join(settings.DATA_DIR, "vida_feed.csv"), index=False)
        VidaAPI.feed_update_date = datetime.now()
        print("Feed updated.")

    def __get_cat_products_feed(self, category):
        if (
            VidaAPI.feed_update_date is None
            or datetime.now() - VidaAPI.feed_update_date > timedelta(hours=1)
        ):
            self.__update_feed()
        data = pd.read_parquet(VidaAPI.feed_path)
        return data[data["Category"].str.contains(category)]

    def __get_cat_products_api(self, category):
        avail_products = self.__get_avail_products_api()
        return [prod for prod in avail_products if category in prod["category_path"]]


class VidaProduct:
    def __init__(
        self,
        sku,
        ean,
        name,
        b2b_price,
        web_shop_price,
        stock,
        category,
        prod_description,
        images,
        properties,
        delivery_time,
    ):
        self.sku = sku
        self.ean = ean
        self.name = name
        self.b2b_price = b2b_price
        self.web_shop_price = web_shop_price
        self.profit = web_shop_price / 1.21 - b2b_price
        self.stock = stock
        self.category = category
        self.description = prod_description
        self.images_urls = images
        self.properties = properties
        self.delivery_time = self.get_delivery_range(delivery_time)
        self.tuned_description = None
        self.tuned_bol_name = None

    def __str__(self):
        return f"{self.name} - {self.web_shop_price} - {self.stock}"

    @staticmethod
    def get_delivery_range(delivery_time):
        if delivery_time == 1:
            return "1-2d"
        elif delivery_time == 2:
            return "2-3d"
        elif 3 <= delivery_time < 5:
            return "3-5 werkdagen"
        elif delivery_time >= 5:
            return "4-8d"
        else:
            return "1-8d"

    def get_tuned_description(self):
        gpt_descriptor = ProductDescriptionGenerator(
            self.name, self.category, self.description, self.properties
        )
        tuned_description = gpt_descriptor.tun_description()
        bol_name = gpt_descriptor.generate_bol_name()
        self.tuned_description = tuned_description
        self.tuned_bol_name = bol_name

    def save_images(self):
        img_dir = os.path.join(
            settings.PROD_MEDIA_DIR, str(self.ean) + "_" + str(self.sku)
        )
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        for img in self.images_urls:
            img_path = os.path.join(img_dir, img.split("/")[-1])
            if os.path.exists(img_path):
                continue
            img_data = requests.get(img).content
            with open(img_path, "wb") as f:
                f.write(img_data)
        return img_dir

    def translate(self, language):
        pass


class OrderFileBuilder:
    ProductsLoaded = 0

    def __init__(self, template_path):
        self.template = template_path
        self.output = os.path.join(settings.DATA_DIR, "order_file.xlsx")
        self.__extension = os.path.basename(self.template).split(".")[-1]

    def load_template(self):
        if self.__extension == "xlsx":
            return pd.read_excel(self.template)
        elif self.__extension == "csv":
            return pd.read_csv(self.template)
        else:
            with open(self.template, "r") as f:
                return f.read()

    def create_order_file(self, order_data):
        if OrderFileBuilder.ProductsLoaded == 0:
            template = self.load_template()
        else:
            template = pd.read_excel(self.output)
        if isinstance(template, pd.DataFrame):
            order_df = pd.DataFrame(order_data, index=[0])
            template = pd.concat([template, order_df], axis=0)
            template.to_excel(self.output, index=False)
        else:
            with open(self.output, "w") as f:
                f.write(template.format(**order_data))
        OrderFileBuilder.ProductsLoaded += 1
        return self.output


class BolFileBuilder(OrderFileBuilder):
    def __init__(
        self,
        template_path=os.path.join(
            settings.BASE_DIR, "data_files", "bol_template.xlsx"
        ),
    ):
        super().__init__(template_path)
        self.output = os.path.join(settings.DATA_DIR, "bol_order_file.xlsx")

    def create_bol_file(self, order_data):
        return super().create_order_file(order_data)


# sku, ean, name, price, stock, category, description, images, properties
if __name__ == "__main__":
    print("stores api file")
    vida = VidaAPI()
    print(vida.product_source)
    products = vida.get_available_products()
    electronics = vida.get_category_products("Elektronica")
    print(len(products))
    print(len(electronics))
