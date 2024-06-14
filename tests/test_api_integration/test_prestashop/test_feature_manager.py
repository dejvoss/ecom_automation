import unittest

from apis_integration.presta_shop.presta_client import PrestashopClient
from apis_integration.presta_shop.managers.feature_manager import FeaturesManager
import settings


# @unittest.skip("Skip for now as it works and testing creates records in database.")
class TestFeaturesManagerRealAPI(unittest.TestCase):
    def setUp(self):
        self.client = PrestashopClient(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )
        self.brand_manager = FeaturesManager(
            self.client
        )

    def test_getting_correct_feature_with_value(self):
        feature_name = "Colours"
        feature_value = "black"
        known_feature_id = 1
        known_feature_value_id = 19
        feature_id, feature_value_id = (
            self.brand_manager.get_or_create_feature_value_pair(
                feature_name, feature_value
            )
        )
        self.assertIsNotNone(feature_id)
        self.assertIsNotNone(feature_value_id)
        self.assertIsInstance(feature_id, int)
        self.assertIsInstance(feature_value_id, int)
        self.assertEqual(feature_id, known_feature_id)
        self.assertEqual(feature_value_id, known_feature_value_id)

    def test_getting_feature_with_wrong_name(self):
        feature_name = "Wrong Name"
        feature_id = self.brand_manager.get_feature(feature_name)
        self.assertIsNone(feature_id)

    def test_getting_feature_value(self):
        feature_value = "black"
        feature_id = 1
        known_feature_value_id = 19
        feature_value_id = self.brand_manager.get_feature_value(
            feature_value, feature_id
        )
        self.assertIsNotNone(feature_value_id)
        self.assertIsInstance(feature_value_id, int)
        self.assertEqual(feature_value_id, known_feature_value_id)

    def test_getting_feature_value_with_wrong_value(self):
        feature_value = "Wrong Value"
        feature_id = 1
        feature_value_id = self.brand_manager.get_feature_value(
            feature_value, feature_id
        )
        self.assertIsNone(feature_value_id)

    def test_create_feature_value(self):
        feature_value = "XL"
        feature_id = 16
        feature_value_id = self.brand_manager.get_or_create_feature_value(
            feature_value, feature_id
        )
        created_feature_value = self.brand_manager.get_feature_value(
            feature_value, feature_id
        )
        self.assertIsNotNone(feature_value_id)
        self.assertIsInstance(feature_value_id, int)
        self.assertGreater(feature_value_id, 0)
        self.assertEqual(feature_value_id, created_feature_value)

    def test_create_feature(self):
        feature_name = "Sizes"
        feature_id = self.brand_manager.get_or_create_feature(feature_name)
        created_feature = self.brand_manager.get_feature(feature_name)
        self.assertIsNotNone(feature_id)
        self.assertIsInstance(feature_id, int)
        self.assertGreater(feature_id, 0)
        self.assertEqual(feature_id, created_feature)
