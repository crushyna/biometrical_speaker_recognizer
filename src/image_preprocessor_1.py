import imagehash
import matplotlib.pyplot as plt
from PIL import Image
# TODO: decide whether to go with WHASH or DHASH
from numpy.core.multiarray import ndarray


class ImagePreprocessor:

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
        print(f'Length: {len(self.stored_image.getvalue())}')

        hash1 = imagehash.dhash(Image.open(self.input_image), hash_size=64)
        hash2 = imagehash.dhash(Image.open(self.stored_image), hash_size=64)

        return hash1 - hash2

    def compare_whash(self):
        hash1 = imagehash.whash(Image.open(self.input_image), hash_size=64)
        hash2 = imagehash.whash(Image.open(self.stored_image), hash_size=64)

        return hash1 - hash2

    @staticmethod
    def generate_audio_image(array: ndarray, buffer_name: str):
        """
        plot image of ndarray and save it into memory buffer
        :param buffer_name: str
        :param array: ndarray
        :return: book, bytesIO
        """
        from io import BytesIO
        buffer_name = BytesIO()

        plt.figure(figsize=(5, 2), frameon=False)
        # plt.axis('off')
        plt.plot(array)
        plt.savefig(buffer_name, format='png', facecolor='white', transparent=False, bbox_inches='tight',
                    pad_inches=0, dpi=300)
        plt.close()

        return isinstance(buffer_name.getvalue(), str), buffer_name
