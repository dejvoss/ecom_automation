import unittest

from apis_integration.presta_shop.managers.stock_manager import StockManager
import settings


# @unittest.skip("Skip for now as it works and testing creates records in database.")
class TestStockManagerRealAPI(unittest.TestCase):
    def setUp(self):
        self.stock_manager = StockManager(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )

    def test_update_stock(self):
        product_id = 28
        stock_qty = 10
        result = self.stock_manager.update_stock(product_id, stock_qty)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertEqual(result, stock_qty)

    def test_get_product_stock_qty(self):
        product_id = 28
        stock_qty = 10
        self.stock_manager.update_stock(product_id, stock_qty)
        result = self.stock_manager.get_product_stock_qty(product_id)
        print(result)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertEqual(result, stock_qty)
