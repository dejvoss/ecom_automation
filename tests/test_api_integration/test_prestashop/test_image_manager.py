import unittest
import os

from apis_integration.presta_shop.managers.base_api import PrestashopClient
from apis_integration.presta_shop.managers.image_manager import (
    ImageManager,
    ImageNotAllowedError,
)
import settings


@unittest.skip("Skip for now as it works and testing creates records in database.")
class TestImageManagerRealAPI(unittest.TestCase):
    def setUp(self):
        self.client = PrestashopClient(
            settings.PRESTASHOP_API_URL,
            api_key=settings.PRESTASHOP_API_TOKEN,
            api_secret=settings.PRESTASHOP_API_SECRET,
        )
        self.image_manager = ImageManager(
            self.client
        )
        self.img_dir = os.path.join(settings.BASE_DIR, "media", "product_images")

    def test_upload_images_from_empty_dir(self):
        product_id = 28
        with self.assertRaises(ImageNotAllowedError):
            self.image_manager.upload_image(product_id, self.img_dir)

    def test_upload_images_from_dir(self):
        product_id = 28
        image_dir = os.path.join(self.img_dir, "8720845579487_813965")
        result = self.image_manager.upload_image(product_id, image_dir)
        self.assertIsNotNone(result)
        self.assertEqual(result, True)

    def test_upload_image_file(self):
        product_id = 28
        image_path = os.path.join(
            self.img_dir, "8720845579487_813965", "8720845579487_m_en_hd_1.jpg"
        )
        result = self.image_manager.upload_image(product_id, image_path)
        self.assertIsNotNone(result)
        self.assertEqual(result, 200)

    def test_upload_image_url(self):
        product_id = 28
        image_url = "https://www.tapeciarnia.pl/fotki/d/25061_1466835266_2843.jpg"
        result = self.image_manager.upload_image(product_id, image_url)
        self.assertIsNotNone(result)
        self.assertEqual(result, 200)

    def test_upload_image_invalid_path(self):
        product_id = 28
        image_path = "invalid_path"
        with self.assertRaises(ValueError):
            self.image_manager.upload_image(product_id, image_path)

    def test_upload_image_not_vaild_format(self):
        product_id = 28
        image_path = os.path.join(
            self.img_dir, "8720845579487_813965", "8720845579487_m_en_hd_1.txt"
        )
        with self.assertRaises(ImageNotAllowedError):
            self.image_manager.upload_image(product_id, image_path)
