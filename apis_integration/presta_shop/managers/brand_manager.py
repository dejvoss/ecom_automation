from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop.managers.base_api import (
    BaseManager,
)
from apis_integration.presta_shop import utils


class BrandManager(BaseManager):

    def get_or_create(self, data: dict):
        existing_brand_id = self.get_id_by_name(data["name"])
        if existing_brand_id is not None:
            print(f"Brand {data['name']} already exists with id nr {existing_brand_id}")
            return existing_brand_id
        return self.__create_brand(data)

    def __create_brand(self, data: dict):
        body = self.__prepare_brand_xml(data)
        response = self.make_post_call("/manufacturers", body)
        if response is not None:
            brand_id = response.find("manufacturer/id").text
            print(f"Brand {data['name']} with id nr {brand_id} added successfully")
            return int(brand_id)

    def __prepare_brand_xml(self, data: dict):
        prestashop = utils.create_prestashop_base_xml()
        brand = self.__create_brand_element(prestashop, data)
        utils.add_seo_xml_sub_elements(brand, data)
        return utils.prettify_xml(prestashop)

    @staticmethod
    def __create_brand_element(parent_element, data: dict):
        brand = SubElement(parent_element, "manufacturer")
        SubElement(brand, "name").text = data["name"]
        SubElement(brand, "active").text = "1"
        utils.create_english_sub_element(brand, "description", data["description"])
        utils.create_english_sub_element(
            brand, "short_description", data["short_description"]
        )
        return brand

    def get_id_by_name(self, brand_name):
        path_url = f"/manufacturers?display=[id]&filter[name]={brand_name}"
        response = self.make_get_call(path_url)
        if response:
            if "manufacturers" in response and len(response["manufacturers"]) > 0:
                return response["manufacturers"][0]["id"]
            else:
                print("No brand with this name found")
                return None
        else:
            print("Failed to fetch brand data or error occurred")
            return None

    def delete_brand(self, brand_name):
        brand_id = self.get_id_by_name(brand_name)
        if brand_id:
            response = self.make_delete_call(f"/manufacturers/{brand_id}")
            if response.status_code == 200:
                print(f"Brand {brand_name} deleted successfully")
                return True
            else:
                print("Brand deletion failed")
        return False
