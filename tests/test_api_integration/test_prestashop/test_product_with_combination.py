import unittest

from apis_integration.presta_shop.presta_client import PrestashopClient
from apis_integration.presta_shop.managers.product_manager import ProductManager
import settings


# @unittest.skip("Skip for now as it works and testing creates records in database.")
class TestCreationProductWithCombination(unittest.TestCase):
    def setUp(self):
        self.client = PrestashopClient(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )
        self.product_manager = ProductManager(
            self.client
        )

    def test_get_or_create(self):
        test_data = {
            "id_manufacturer": "1",
            "id_supplier": "0",
            "id_category_default": "3",
            "is_new": "1",
            "id_default_combination": "1",
            "id_tax_rules_group": "53",
            "type": "1",
            "id_shop_default": "1",
            "reference": "test44585",
            "supplier_reference": "44585",
            "ean13": "1234567891234",
            "state": "1",
            "product_type": "combinations",
            "price": "23.45",
            "unit_price": "23.45",
            "is_active": "0",
            "name": "Test Combination Product",
            "description": "Combination product",
            "short_description": "Combi Product",
            "meta_title": "Product with combinations",
            "meta_description": "Combination Test Product",
            "meta_keywords": "Combination, Meta, Test, Product, oftionn, Keywords",
            "category_id": "3",
        }

        result = self.product_manager.get_or_create(test_data)
        print(result)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
