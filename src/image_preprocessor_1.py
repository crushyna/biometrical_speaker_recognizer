from PIL import Image
import imagehash


# so its WHASH or DHASH - only those make sens

class ImagePreprocessor:

    def __init__(self, input_image, stored_image):
        self.input_image = f'{input_image}.png'
        self.stored_image = stored_image

    def get_input_image(self):
        pass

    def get_stored_image(self):
        pass

    def compare_dhash(self):
        hash1 = imagehash.dhash(Image.open(self.input_image))
        hash2 = imagehash.dhash(Image.open(self.stored_image))

        return hash1 - hash2

    def compare_whash(self):
        hash1 = imagehash.whash(Image.open(self.input_image))
        hash2 = imagehash.whash(Image.open(self.stored_image))

        return hash1 - hash2
