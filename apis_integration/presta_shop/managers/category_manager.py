from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop.managers.base_api import (
    BaseManager,
)
from apis_integration.presta_shop import utils


class CategoryManager(BaseManager):

    def get_or_create(self, data: dict):
        existing_category_id = self.get_category_id_by_name(data["name"])
        if existing_category_id is not None:
            print(
                f"Category {data['name']} already exists with id nr {existing_category_id}"
            )
            return existing_category_id
        return self.__create_category(data)

    def __create_category(self, data: dict):
        body = self.__prepare_category_xml(data)
        response = self.make_post_call("/categories", body)
        if response is not None:
            category_id = response.find("category/id").text
            print(
                f"Category {data['name']} with id nr {category_id} added successfully"
            )
            return int(category_id)

    def __prepare_category_xml(self, data: dict):
        prestashop = utils.create_prestashop_base_xml()
        category = self.__create_category_element(prestashop, data)
        utils.add_seo_xml_sub_elements(category, data)
        return utils.prettify_xml(prestashop)

    @staticmethod
    def __create_category_element(parent_element, data: dict):
        category = SubElement(parent_element, "category")
        utils.create_english_sub_element(category, "name", data["name"])
        utils.create_english_sub_element(
            category, "link_rewrite", data["name"].replace(" ", "-")
        )
        utils.create_english_sub_element(category, "description", data["description"])
        SubElement(category, "active").text = data["is_active"]
        SubElement(category, "id_parent").text = data["id_parent"]
        return category

    def get_category_id_by_name(self, category_name):
        path_url = f"/categories?display=[id]&filter[name]={category_name}"
        response = self.make_get_call(path_url)
        if response:
            if "categories" in response and len(response["categories"]) > 0:
                return response["categories"][0]["id"]
            else:
                print("No category with this name found")
                return None
        else:
            print("Failed to fetch category data or error occurred")
            return None

    def delete_category(self, category_name):
        category_id = self.get_category_id_by_name(category_name)
        if category_id:
            response = self.make_delete_call(f"/categories/{category_id}")
            if response.status_code == 200:
                print(f"Category {category_name} deleted successfully")
                return True
            else:
                print(f"Failed to delete category {category_name}")
                return False
        else:
            print(f"Category {category_name} not found")
            return False
