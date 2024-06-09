from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop.managers.base_api import (
    PrestashopGetter,
    PrestashopPoster,
)

from apis_integration.presta_shop import utils


class FeaturesManager(PrestashopPoster, PrestashopGetter):
    def get_or_create_feature_value_pair(self, feature_name, feature_value):
        feature_id = self.get_or_create_feature(feature_name)
        feature_value_id = self.get_or_create_feature_value(feature_value, feature_id)

        return feature_id, feature_value_id

    def get_or_create_feature(self, feature_name):
        feature_id = self.get_feature(feature_name)
        if feature_id is not None:
            return feature_id
        else:
            return self.__create_feature(feature_name)

    def get_or_create_feature_value(self, feature_value, feature_id):
        feature_value_id = self.get_feature_value(feature_value, feature_id)
        if feature_value_id is not None:
            return feature_value_id
        else:
            return self.__create_feature_value(feature_value, feature_id)

    def get_feature(self, feature_name):
        path_url = f"/product_features?display=[id]&filter[name]={feature_name}"
        response = self.make_get_call(path_url)
        if response:
            if "product_features" in response and len(response["product_features"]) > 0:
                return response["product_features"][0]["id"]
            else:
                print("No feature with this name found")
                return None
        else:
            print("Failed to fetch feature data or error occurred")
            return None

    def __create_feature(self, feature_name):
        body = self.__prepare_feature_xml(feature_name)
        response = self.make_post_call("/product_features", body)
        if response is not None:
            feature_id = response.find("product_feature/id").text
            print(f"Feature {feature_name} with id nr {feature_id} added successfully")
            return int(feature_id)

    @staticmethod
    def __prepare_feature_xml(feature_name):
        prestashop_element = utils.create_prestashop_base_xml()
        product_feature = SubElement(prestashop_element, "product_feature")
        utils.create_english_sub_element(product_feature, "name", feature_name)
        return utils.prettify_xml(prestashop_element)

    def get_feature_value(self, feature_value, feature_id):
        path_url = f"/product_feature_values/?display=[id]&filter[id_feature]={feature_id}&filter[value]={feature_value}"
        response = self.make_get_call(path_url)
        if response:
            if (
                "product_feature_values" in response
                and len(response["product_feature_values"]) > 0
            ):
                return response["product_feature_values"][0]["id"]
            # maybe [product_feature_values][product_feature_value][0]["id"]
            else:
                print("No feature value with this name found")
                return None
        else:
            print("Failed to fetch feature value data or error occurred")
            return None

    def __create_feature_value(self, feature_value, feature_id):
        body = self.__prepare_feature_value_xml(feature_value, feature_id)
        response = self.make_post_call("/product_feature_values", body)
        if response is not None:
            feature_value_id = response.find("product_feature_value/id").text
            print(
                f"Feature value {feature_value} with id nr {feature_value_id} added successfully"
            )
            return int(feature_value_id)

    @staticmethod
    def __prepare_feature_value_xml(value, feature_id):
        prestashop_element = utils.create_prestashop_base_xml()
        product_feature_value = SubElement(prestashop_element, "product_feature_value")
        SubElement(product_feature_value, "id_feature").text = str(feature_id)
        utils.create_english_sub_element(product_feature_value, "value", value)
        return utils.prettify_xml(prestashop_element)
