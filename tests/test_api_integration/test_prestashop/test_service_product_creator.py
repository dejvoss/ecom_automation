from unittest import TestCase
from apis_integration.presta_shop.presta_client import PrestashopClient
from apis_integration.presta_shop.services import ServiceProductCreator

import settings


class TestServiceProductCreator(TestCase):
    def setUp(self):
        self.client = PrestashopClient(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )
        self.cleared_product_data = {
            "id_manufacturer": 1,
            "id_supplier": 1,
            "id_category_default": 2,
            "new": 1,
            "id_default_combination": 0,
            "id_tax_rules_group": 1,
            "type": "standard",
            "id_shop_default": 1,
            "reference": 11,
            "supplier_reference": "",
            "ean13": "",
            "state": 1,
            "product_type": 0,
            "price": 100,
            "unit_price": "",
            "active": True,
            "name": "Test Product",
            "description": "This is a test product",
            "short_description": "",
            "meta_title": "Test Product",
            "meta_description": "",
            "meta_keywords": "",
            "categories_id": [2,3],
            "features": [
                {"feature_id": 1, "value_id": 1},
                {"feature_id": 2, "value_id": 2},
            ],
        }

        self.product_data = {
            "manufacturer": "Test brand",
            "supplier": "Test supplier",
            "categories": ["Test category", "Test category 2"],
            "new": "1",
            "default_combination": "1",
            "tax_rules_group": "53",
            "type": "1",
            "shop_default": "1",
            "reference": "test44585",
            "supplier_reference": "44585",
            "ean13": "1234567891234",
            "state": "1",
            "product_type": "standard",
            "price": "23.45",
            "unit_price": "23.45",
            "active": "0",
            "name": "Test Product",
            "description": "Test Product Description",
            "short_description": "Test Product short description",
            "meta_title": "Test Product",
            "meta_description": "Test Product meta desc",
            "meta_keywords": "Test, Product, oftionn, Keywords",
            "features": {
                "color": "blue",
                "battery life": "11 hours",
                "connection": "wifi",
            },
        }

