from apis_integration.presta_shop.managers import *


class ServiceProductCreator:
    def __init__(self, product_data, client):
        self.product_data = product_data
        self.product_manager = ProductManager(client)
        self.category_manager = CategoryManager(client)
        self.image_manager = ImageManager(client)
        self.combination_manager = CombinationsManager(client)
        self.stock_manager = StockManager(client)
        self.product_feature_manager = FeaturesManager(client)

    def validate_product_data(self):
        pass

# TODO: Create Product Data Validator or function for validating product data
# TODO: Product Data Creator - for missing data - this will rrequire GPT or some other AI
# TODO: Product Creator - for creating product
# TODO: As it require gpt - it cannot be in apis integration / prestashop. It should be in a separate module.
# TODO: Here will be only the product creator service - which will use diferrent managers to create product.
# TODO: The data validator here will be just raise an exception. To service work, data needs to be provided.
# TODO: Start from writing the test for this service - this will gives the idea of what data needs to be provided.
