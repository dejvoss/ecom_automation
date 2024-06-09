import unittest

from apis_integration.presta_shop.managers.attributes_manager import AttributeManager
import settings


class TestAttributeManager(unittest.TestCase):
    def setUp(self):
        self.attribute_manager = AttributeManager(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )

    def test_get_or_create_attribute_id(self):
        attribute = self.attribute_manager.get_attribute_id("test_size")
        self.assertIsInstance(attribute, int)
        self.assertEqual(attribute, 129)

    def test_get_non_existed_attribute_id(self):
        attribute = self.attribute_manager.get_attribute_id("imagination")
        self.assertIsNone(attribute, None)

    def test_getting_attribute_value_id(self):
        attribute_value = self.attribute_manager.get_attribute_value_id(2, "black")
        self.assertIsInstance(attribute_value, int)
        self.assertEqual(attribute_value, 4)

    def test_get_or_create_attribute_value(self):
        attribute_value = self.attribute_manager.get_or_create_attribute_value(
            2, "elegant black"
        )
        self.assertIsInstance(attribute_value, int)
        self.assertEqual(attribute_value, 2)

    def test_get_non_existed_attribute_value(self):
        attribute_value = self.attribute_manager.get_attribute_value_id(
            2, "imagination"
        )
        self.assertIsNone(attribute_value, None)

    def test_get_existed_id_product_attribute_value_by_attribute_pair(self):
        attribute_pair = self.attribute_manager.get_id_product_attribute_value(
            "color", "color", "elegant black"
        )
        self.assertIsInstance(attribute_pair, int)
        self.assertEqual(attribute_pair, 2)

    def test_get_product_attribute_value_by_attribute_pair_not_existing(self):
        attribute_pair = self.attribute_manager.get_id_product_attribute_value(
            "color", "color", "gray"
        )
        self.assertIsInstance(attribute_pair, int)
        self.assertEqual(attribute_pair, 12)

    def test_get_new_product_attribute_value_by_attribute_pair_not_existing(self):
        attribute_pair = self.attribute_manager.get_id_product_attribute_value(
            "color", "color", "cyan"
        )
        self.assertIsInstance(attribute_pair, int)
        self.assertEqual(attribute_pair, 13)
