import unittest

from apis_integration.presta_shop.managers.product_manager import ProductManager
import settings


# @unittest.skip("Skip for now as it works and testing creates records in database.")
class TestProductManagerRealAPI(unittest.TestCase):
    def setUp(self):
        self.product_manager = ProductManager(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )

    def test_get_product_id_by_name(self):
        product_name = 'Wall Mounted Network Cabinet 19" IP20'
        product_id = self.product_manager.get_product_id_by(name=product_name)
        print(product_id)
        self.assertIsNotNone(product_id)
        self.assertIsInstance(product_id, int)
        self.assertEqual(product_id, 7)

    def test_get_product_id_by_reference(self):
        product_reference = "WMC-6U-300"
        product_id = self.product_manager.get_product_id_by(reference=product_reference)
        print(product_id)
        self.assertIsNotNone(product_id)
        self.assertIsInstance(product_id, int)
        self.assertEqual(product_id, 7)

    def test_get_product_id_by_ean13(self):
        product_ean13 = "6948541721371"
        product_id = self.product_manager.get_product_id_by(ean13=product_ean13)
        print(product_id)
        self.assertIsNotNone(product_id)
        self.assertIsInstance(product_id, int)
        self.assertEqual(product_id, 4)

    def test_get_product_id_by_invalid_filter(self):
        with self.assertRaises(ValueError):
            self.product_manager.get_product_id_by(invalid_filter="invalid_filter")

    def test_get_product_id_by_many_filters(self):
        product_name = "Let's Encrypt AutoSSL Wizard by Certbot"
        product_reference = "LEASSL"
        product_ean13 = "1118541721371"
        product_id = self.product_manager.get_product_id_by(
            name=product_name, reference=product_reference, ean13=product_ean13
        )
        print(product_id)
        self.assertIsNotNone(product_id)
        self.assertIsInstance(product_id, int)
        self.assertEqual(product_id, 1)

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
            "product_type": "standard",
            "price": "23.45",
            "unit_price": "23.45",
            "is_active": "0",
            "name": "Test Product",
            "description": "Test Product",
            "short_description": "Test Product",
            "meta_title": "Test Product",
            "meta_description": "Test Product",
            "meta_keywords": "Test, Product, oftionn, Keywords",
            "category_id": ["3", "198"],
            "features": [
                {"feature_id": "1", "value_id": "1"},
                {"feature_id": "1", "value_id": "2"},
                {"feature_id": "15", "value_id": "25"},
            ],
        }

        result = self.product_manager.get_or_create(test_data)
        print(result)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
