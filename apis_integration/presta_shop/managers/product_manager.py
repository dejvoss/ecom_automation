from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop.managers.base_api import (
    BaseManager,
    PrestashopGetter,
)
from apis_integration.presta_shop import utils


class ProductManager(BaseManager):

    def get_or_create(self, data: dict):
        existing_product_id = self.get_product_id_by(name=data["name"])
        if existing_product_id is not None:
            print(
                f"Product {data['name']} already exists with id nr {existing_product_id}"
            )
            return existing_product_id
        return self.__create_product(data)

    def get_product_id_by(self, **kwargs):
        self.__product_key_validate(kwargs)
        path_url = "/products?display=[id]"
        for key, value in kwargs.items():
            path_url += f"&filter[{key}]={value}"
        response = self.make_get_call(path_url)
        if response:
            if "products" in response and len(response["products"]) > 0:
                return response["products"][0]["id"]
            else:
                print("No product with this name found")
                return None
        else:
            print("Failed to fetch product data or error occurred")
            return None

    @staticmethod
    def __product_key_validate(kwargs):
        keys = [key for key in kwargs.keys()]
        correct_keys = ["name", "reference", "ean13"]
        filtered_keys = filter(lambda key: key not in correct_keys, keys)
        if len(list(filtered_keys)) > 0:
            raise ValueError("Invalid filter key provided")

    def __create_product(self, data: dict):
        body = self.__prepare_product_xml(data)
        response = self.make_post_call("/products", body)

        if response is not None:
            created_product_id = response.find("product/id").text
            print(
                f"Product {data['name']} with id nr {created_product_id} added successfully"
            )
            return int(created_product_id)

    def __prepare_product_xml(self, data: dict):
        prestashop = utils.create_prestashop_base_xml()
        product = self.__create_product_element(prestashop, data)
        utils.add_seo_xml_sub_elements(product, data)
        self.__add_associations_xml_sub_elements(product, data)
        return utils.prettify_xml(prestashop)

    @staticmethod
    def __create_product_element(parent_element, data: dict):
        product = SubElement(parent_element, "product")
        SubElement(product, "id_manufacturer").text = data["id_manufacturer"]
        SubElement(product, "id_supplier").text = data["id_supplier"]
        SubElement(product, "id_category_default").text = data["id_category_default"]
        SubElement(product, "new").text = data["is_new"]
        SubElement(product, "id_default_combination").text = data[
            "id_default_combination"
        ]
        SubElement(product, "id_tax_rules_group").text = data["id_tax_rules_group"]
        SubElement(product, "type").text = data["type"]
        SubElement(product, "id_shop_default").text = data["id_shop_default"]
        SubElement(product, "reference").text = data["reference"]
        SubElement(product, "supplier_reference").text = data["supplier_reference"]
        SubElement(product, "ean13").text = data["ean13"]
        SubElement(product, "state").text = data["state"]
        SubElement(product, "product_type").text = data[
            "product_type"
        ]  # standard, combination, virtual
        SubElement(product, "price").text = data["price"]
        SubElement(product, "unit_price").text = data["unit_price"]
        SubElement(product, "active").text = data["is_active"]

        utils.create_english_sub_element(product, "name", data["name"])
        utils.create_english_sub_element(product, "description", data["description"])
        utils.create_english_sub_element(
            product, "description_short", data["short_description"]
        )
        return product

    @staticmethod
    def __add_associations_xml_sub_elements(product_element, data):
        associations = SubElement(product_element, "associations")
        categories = SubElement(associations, "categories")
        for cat_id in data["category_id"]:
            category = SubElement(categories, "category")
            SubElement(category, "id").text = cat_id
        features = SubElement(associations, "product_features")
        for feature in data["features"]:
            feature_element = SubElement(features, "product_feature")
            SubElement(feature_element, "id").text = feature["feature_id"]
            SubElement(feature_element, "id_feature_value").text = feature["value_id"]
        return product_element
