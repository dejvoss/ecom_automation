from xml.etree.ElementTree import SubElement

from apis_integration.presta_shop.managers.base_api import (
    PrestashopGetter,
    PrestashopPatcher,
)
from apis_integration.presta_shop import utils


class StockManager(PrestashopGetter, PrestashopPatcher):
    def update_stock(self, product_id, stock_qty):
        stock_availables_id = self.__get_stock_availability_id_for_product(product_id)
        prestashop = utils.create_prestashop_base_xml()
        stock_element = SubElement(prestashop, "stock_available")
        SubElement(stock_element, "id").text = str(stock_availables_id)
        SubElement(stock_element, "quantity").text = str(stock_qty)
        body = utils.prettify_xml(prestashop)
        response = self.make_patch_call(f"/stock_availables/{product_id}", body)
        if response is not None:
            updated_stock = response.find("stock_available/quantity").text
            print(f"Stock for product {product_id} updated successfully")
            print("Current stock: ", updated_stock)
            return int(updated_stock)
        else:
            print(f"Failed to update stock for product {product_id}")
            return None

    def __get_stock_availability_id_for_product(self, product_id):
        url = f"/stock_availables?filter[id_product]={product_id}&display=[id]"
        response = self.make_get_call(url)
        if response:
            if "stock_availables" in response and len(response["stock_availables"]) > 0:
                return response["stock_availables"][0]["id"]
            else:
                print("No stock availability data found for this product")
                return None
        else:
            print("Failed to fetch stock availability data or error occurred")
            return None

    def get_product_stock_qty(self, product_id):
        stock_availables_id = self.__get_stock_availability_id_for_product(product_id)
        url = f"/stock_availables/{stock_availables_id}"
        response = self.make_get_call(url)
        if response:
            if "stock_available" in response:
                return response["stock_available"]["quantity"]
            else:
                print("No stock availability data found for this product")
                return None
        else:
            print("Failed to fetch stock availability data or error occurred")
            return None
