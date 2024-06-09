import unittest

from apis_integration.presta_shop.managers.brand_manager import BrandManager
import settings


# @unittest.skip("Skip for now as it works and testing creates records in database.")
class TestBrandManagerRealAPI(unittest.TestCase):
    def setUp(self):
        self.brand_manager = BrandManager(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )

    def test_get_or_create(self):
        test_data = {
            "name": "Test Brand",
            "description": "Brand for testing status change",
            "short_description": "Test Short Description",
            "meta_title": "Test Meta Title",
            "meta_description": "Test Meta Description",
            "meta_keywords": "Test, Meta, brand, Keywords, oftionn",
        }
        result = self.brand_manager.get_or_create(test_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_get_brand_id_by_name(self):
        result = self.brand_manager.get_id_by_name("oftionn")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_delete_brand(self):
        result = self.brand_manager.delete_brand("Test Brand")
        self.assertEqual(result, True)
        self.assertIsNone(self.brand_manager.get_id_by_name("Test Brand"))
