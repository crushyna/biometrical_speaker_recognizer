from PIL import Image
import imagehash


# so its WHASH or DHASH - only those make sens

class ImagePreprocessor:

    def __init__(self, input_image, stored_image):
        self.input_image = input_image
        self.stored_image = stored_image

    def get_input_image(self):
        pass

    def get_stored_image(self):
        pass

    def compare_dhash(self, image1, image2):
        hash1 = imagehash.dhash(Image.open(image1))
        hash2 = imagehash.dhash(Image.open(image2))

        return hash1 - hash2

    def compare_whash(self, image1, image2):
        hash1 = imagehash.whash(Image.open(image1))
        hash2 = imagehash.whash(Image.open(image2))

        return hash1 - hash2
