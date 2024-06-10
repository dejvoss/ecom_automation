from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop import utils
from apis_integration.presta_shop.managers import base_api


class CombinationsManager(base_api.BaseManager):

    def get_or_create_combination(self, data: dict):
        combination_id = self.get_combination_id_by(
            data["id_product"], data["id_product_attribute"]
        )
        if combination_id:
            return combination_id
        return self.create_combination(data)

    def get_combination_id_by(self, product_id, id_product_attribute):
        path_url = f"/combinations?display=full&filter[id_product]={product_id}"
        response = self.make_get_call(path_url)
        if response:

            if "combinations" in response and len(response["combinations"]) > 0:
                for combination in response["combinations"]:
                    attribute_id = combination["associations"]["product_option_values"][
                        0
                    ]["id"]
                    print(attribute_id)
                    if attribute_id == id_product_attribute:
                        return combination["id"]

        return None

    def get_product_attribute_id_by_combination(self, combination_id):
        path_url = f"/combinations/{combination_id}"
        response = self.make_get_call(path_url)
        if response:
            if "combination" in response:
                return response["combination"]["associations"]["product_option_values"][
                    "product_option_value"
                ]["id"]
        return None

    def create_combination(self, data: dict):
        body = self.__prepare_combination_xml(data)
        response = self.make_post_call("/combinations", body)
        return int(response.find("combination/id").text)

    @staticmethod
    def __prepare_combination_xml(data):
        prestashop = utils.create_prestashop_base_xml()
        combination = SubElement(prestashop, "combination")
        SubElement(combination, "id_product").text = str(data["id_product"])
        SubElement(combination, "ean13").text = data["EAN"]
        SubElement(combination, "mpn").text = data["MPN"] if "MPN" in data else ""
        SubElement(combination, "reference").text = data["reference"]
        SubElement(combination, "supplier_reference").text = data["sku"]
        SubElement(combination, "price").text = str(data["price"])
        SubElement(combination, "minimal_quantity").text = (
            data["minimal_quantity"] if "minimal_quantity" in data else "1"
        )
        associations = SubElement(combination, "associations")
        product_option_values = SubElement(
            associations,
            "product_option_values",
            {"nodeType": "product_option_value", "api": "product_option_values"},
        )
        product_option_value = SubElement(product_option_values, "product_option_value")
        SubElement(product_option_value, "id").text = str(data["id_product_attribute"])
        return utils.prettify_xml(prestashop)
