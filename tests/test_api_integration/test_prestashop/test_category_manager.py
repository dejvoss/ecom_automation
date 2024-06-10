import unittest

from apis_integration.presta_shop.managers.base_api import PrestashopClient
from apis_integration.presta_shop.managers.category_manager import CategoryManager
import settings


# @unittest.skip("Skip for now as it works and testing creates records in database.")
class TestCategoryManagerRealAPI(unittest.TestCase):
    def setUp(self):
        self.client = PrestashopClient(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )
        self.brand_manager = CategoryManager(
            self.client
        )

    def test_create_category(self):
        category_data = {
            "name": "Test Category",
            "description": "This is a test category",
            "is_active": "1",
            "id_parent": "2",
            "meta_title": "Test Category",
            "meta_description": "Test Category",
            "meta_keywords": "Test Category",
        }
        category_id = self.brand_manager.get_or_create(category_data)
        print(category_id)
        self.assertIsNotNone(category_id)
        self.assertIsInstance(category_id, int)
        self.assertGreater(category_id, 0)

    def test_get_category_id_by_name(self):
        category_name = "Curated Picks"
        category_id = self.brand_manager.get_category_id_by_name(category_name)
        print(category_id)
        self.assertIsNotNone(category_id)
        self.assertIsInstance(category_id, int)
        self.assertGreater(category_id, 0)

    def test_delete_category(self):
        category_name = "Test Category"
        result = self.brand_manager.delete_category(category_name)
        self.assertEqual(result, True)
        self.assertIsNone(self.brand_manager.get_category_id_by_name(category_name))
