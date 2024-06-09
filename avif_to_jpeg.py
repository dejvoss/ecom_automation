from PIL import Image
import pillow_avif
import os

# Path to the directory containing the AVIF files
path = r'C:\Users\DeOs\Pictures\ecom\products'

avi_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.avif')]

for file in avi_files:
    img = Image.open(file)
    img.save(file.replace('.avif', '.jpg'), 'JPEG')
    img.close()
    os.remove(file)

