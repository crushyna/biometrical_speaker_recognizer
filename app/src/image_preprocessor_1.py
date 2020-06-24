import imagehash
import matplotlib.pyplot as plt
from PIL import Image
from numpy.core.multiarray import ndarray


class ImagePreprocessor:
    hash_size = 32

    def __init__(self, input_image, stored_image):
        self.input_image = input_image
        self.stored_image = stored_image

    def get_input_image(self):
        pass

    def get_stored_image(self):
        pass

    def compare_dhash(self):
        print(f'Input image: {self.input_image}')
        print(type(self.input_image))
        print(f'Stored image: {self.stored_image}')
        print(type(self.stored_image))

        hash1 = imagehash.dhash(Image.open(self.input_image), hash_size=ImagePreprocessor.hash_size)
        hash2 = imagehash.dhash(Image.open(self.stored_image), hash_size=ImagePreprocessor.hash_size)
        # hash1 = imagehash.dhash_vertical(Image.open(self.input_image), hash_size=ImagePreprocessor.hash_size)
        # hash2 = imagehash.dhash_vertical(Image.open(self.stored_image), hash_size=ImagePreprocessor.hash_size)

        return hash2 - hash1
        # return result

    def compare_whash(self):
        hash1 = imagehash.whash(Image.open(self.input_image), hash_size=ImagePreprocessor.hash_size)
        hash2 = imagehash.whash(Image.open(self.stored_image), hash_size=ImagePreprocessor.hash_size)

        return hash2 - hash1
        # return result

    @staticmethod
    def generate_audio_image(array: ndarray):
        """
        plot image of ndarray and save it into memory buffer
        :param array: ndarray
        :return: book, bytesIO
        """
        from io import BytesIO
        image_buffer = BytesIO()

        plt.figure(figsize=(3, 1), frameon=False)
        plt.axis('off')
        plt.plot(array)
        plt.savefig(image_buffer, format='png', facecolor='white', transparent=False, bbox_inches='tight',
                    pad_inches=0, dpi=200)
        plt.close()

        return isinstance(image_buffer.getvalue(), str), image_buffer
