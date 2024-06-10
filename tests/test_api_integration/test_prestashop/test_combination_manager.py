import unittest

from apis_integration.presta_shop.managers.base_api import PrestashopClient
from apis_integration.presta_shop.managers.combinations_manager import (
    CombinationsManager,
)
import settings


class TestAttributeManager(unittest.TestCase):
    def setUp(self):
        self.client = PrestashopClient(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )
        self.attribute_manager = CombinationsManager(
            self.client
        )
        self.data = {
            "id_product": 26,
            "EAN": "1234567890123",
            "MPN": "12345",
            "reference": "123456",
            "sku": "123456",
            "price": 100,
            "id_product_attribute": 2,
        }

    @unittest.skip("Skipping")
    def test_create_combination(self):
        combination_id = self.attribute_manager.create_combination(self.data)
        self.assertIsInstance(combination_id, int)
        self.assertEqual(combination_id, 16)

    def test_get_combination_id(self):
        combination_id = self.attribute_manager.get_combination_id_by(26, 2)
        self.assertIsInstance(combination_id, int)
        self.assertEqual(combination_id, 16)
