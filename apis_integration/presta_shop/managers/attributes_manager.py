from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop.managers import base_api

from apis_integration.presta_shop import utils


class AttributeManager(base_api.PrestashopGetter, base_api.PrestashopPoster):

    def get_id_product_attribute_value(
        self, attribute_name, attribute_type, attribute_value
    ):
        try:
            attribute_id = self.get_or_create_attribute(attribute_name, attribute_type)
            value_id = self.get_or_create_attribute_value(attribute_id, attribute_value)
        except Exception as e:
            print(f"Error while getting attribute value id: {e}")
            return None
        else:
            return value_id

    def get_or_create_attribute(self, name, attribute_type):
        existed_attribute_id = self.get_attribute_id(name)
        if existed_attribute_id:
            return existed_attribute_id
        else:
            return self.create_attribute(name, attribute_type)

    def get_attribute_id(self, name):
        response = self.make_get_call(f"/product_options?filter[name]={name}")
        if len(response) == 0:
            return None
        return int(response["product_options"][0]["id"])

    def create_attribute(self, name, attribute_type):
        body = self.__prepare_attribute_xml(name, attribute_type)
        response = self.make_post_call("/product_options", body)
        return int(response.find("product_option/id").text)

    @staticmethod
    def __prepare_attribute_xml(name, attribute_type):
        if attribute_type not in ["color", "select", "radio"]:
            raise ValueError("Invalid attribute type")
        prestashop = utils.create_prestashop_base_xml()
        product_option = SubElement(prestashop, "product_option")
        SubElement(product_option, "is_color_group").text = (
            "1" if attribute_type == "color" else "0"
        )
        SubElement(product_option, "group_type").text = attribute_type
        utils.create_english_sub_element(product_option, "name", name)
        utils.create_english_sub_element(product_option, "public_name", name)
        return utils.prettify_xml(prestashop)

    def get_or_create_attribute_value(self, attribute_id, value):
        existed_value_id = self.get_attribute_value_id(attribute_id, value)
        if existed_value_id:
            return existed_value_id
        else:
            return self.create_attribute_value(attribute_id, value)

    def get_attribute_value_id(self, attribute_id, value):
        response = self.make_get_call(
            f"/product_option_values?filter[id_attribute_group]={attribute_id}&filter[name]={value.replace(' ', '+')}"
        )
        print(response)
        if len(response) == 0:
            return None
        return int(response["product_option_values"][0]["id"])

    def create_attribute_value(self, attribute_id, value):
        body = self.__prepare_attribute_value_xml(attribute_id, value)
        response = self.make_post_call("/product_option_values", body)
        print(attribute_id, value, response)
        return int(response.find("product_option_value/id").text)

    @staticmethod
    def __prepare_attribute_value_xml(attribute_id, value):
        prestashop = utils.create_prestashop_base_xml()
        product_option_value = SubElement(prestashop, "product_option_value")
        SubElement(product_option_value, "id_attribute_group").text = str(attribute_id)
        utils.create_english_sub_element(product_option_value, "name", value)
        return utils.prettify_xml(prestashop)
