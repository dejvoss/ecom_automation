import os.path
import requests

from apis_integration.presta_shop.managers.base_api import BaseManager
import settings


class ImageManager(BaseManager):
    def upload_image(self, product_id, image):
        url = f"/images/products/{product_id}"
        if os.path.isfile(image):
            image_file = image
            if not image_file.endswith(settings.IMG_FILE_ALLOWED_EXTENSIONS):
                raise ImageNotAllowedError("Invalid image format provided")
            return self.__upload_image_file(url, image_file)
        elif os.path.isdir(image):
            image_dir = image
            files = [os.path.join(image_dir, file) for file in os.listdir(image_dir)]
            image_files = list(
                filter(
                    lambda file: file.endswith(settings.IMG_FILE_ALLOWED_EXTENSIONS),
                    files,
                )
            )
            if len(image_files) == 0:
                raise ImageNotAllowedError("Invalid images format provided")
            files_uploaded = []
            for image_file in image_files:
                if self.__upload_image_file(url, image_file):
                    files_uploaded.append(image_file)
            return len(files_uploaded) == len(image_files)
        elif image.startswith("http"):
            img_response = requests.get(image).content
            files = {"image": (image, img_response, "image/jpeg")}
            response = self.make_post_files_call(url, files=files)
            if response.status_code == 200:
                print("Image uploaded successfully")
                return response.status_code
            else:
                print("Failed to upload image")
                return False
        else:
            raise ValueError("Invalid image path provided")

    def __upload_image_file(self, url, image_file):
        with open(image_file, "rb") as file:
            image_data = file.read()
        files = {"image": (image_file, image_data, "image/jpeg")}
        response = self.make_post_files_call(url, files=files)
        if response.status_code == 200:
            print("Image uploaded successfully")
            return response.status_code
        else:
            print("Failed to upload image")
            return False


class ImageNotAllowedError(Exception):
    pass
