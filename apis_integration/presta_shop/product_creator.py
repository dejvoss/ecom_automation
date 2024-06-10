from apis_integration.presta_shop.managers import *


class ProductCreator:
    def __init__(self, product_data):
        self.product_data = product_data
        self.product_manager = ProductManager()
        self.category_manager = CategoryManager()
        self.image_manager = ImageManager()
        self.combination_manager = CombinationManager()
        self.stock_manager = StockManager()
        self.price_manager = PriceManager()
        self.product_feature_manager = ProductFeatureManager()
