from PIL import Image
import imagehash


# so its WHASH or DHASH - only those make sens
# TODO: decide whether to go with WHASH or DHASH

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

        hash1 = imagehash.dhash(Image.open(self.input_image), hash_size=64)
        hash2 = imagehash.dhash(Image.open(self.stored_image), hash_size=64)

        return hash1 - hash2

    def compare_whash(self):
        hash1 = imagehash.whash(Image.open(self.input_image), hash_size=64)
        hash2 = imagehash.whash(Image.open(self.stored_image), hash_size=64)

        return hash1 - hash2

    @staticmethod
    def test_comparison():
        """
        for test purposes only!
        """
        test1 = ImagePreprocessor('src/sound_images/inez_1a', 'src/sound_images/inez_1b.png')
        test2 = ImagePreprocessor('src/sound_images/inez_1a', 'src/sound_images/paulina_1a.png')
        test3 = ImagePreprocessor('src/sound_images/maciej_1a', 'src/sound_images/maciej_1b.png')
        test4 = ImagePreprocessor('src/sound_images/maciej_1a', 'src/sound_images/wojtek_1a.png')
        test5 = ImagePreprocessor('src/sound_images/wojtek_1a', 'src/sound_images/wojtek_1b.png')
        test6 = ImagePreprocessor('src/sound_images/wojtek_1a', 'src/sound_images/radek_1b.png')
        test7 = ImagePreprocessor('src/sound_images/radek_1a', 'src/sound_images/radek_1b.png')
        test8 = ImagePreprocessor('src/sound_images/radek_1a', 'src/sound_images/maciej_1b.png')

        print(f'Inez A vs Inez B DHASH: {test1.compare_dhash()}')
        print(f'Inez A vs Inez B WHASH: {test1.compare_whash()}')
        print(f'Inez A vs Paulina B DHASH: {test2.compare_dhash()}')
        print(f'Inez A vs Paulina B WHASH: {test2.compare_whash()}')
        print(f'Maciej A vs Maciej B DHASH: {test3.compare_dhash()}')
        print(f'Maciej A vs Maciej B WHASH: {test3.compare_whash()}')
        print(f'Maciej A vs Wojtek A DHASH: {test4.compare_dhash()}')
        print(f'Maciej A vs Wojtek A WHASH: {test4.compare_whash()}')
        print(f'Wojtek A vs Wojtek B DHASH: {test5.compare_dhash()}')
        print(f'Wojtek A vs Wojtek B WHASH: {test5.compare_whash()}')
        print(f'Wojtek A vs Radek B DHASH: {test6.compare_dhash()}')
        print(f'Wojtek A vs Radek B WHASH: {test6.compare_whash()}')
        print(f'Radek A vs Radek B DHASH: {test7.compare_dhash()}')
        print(f'Radek A vs Radek B WHASH: {test7.compare_whash()}')
        print(f'Radek A vs Maciej B DHASH: {test8.compare_dhash()}')
        print(f'Radek A vs Maciej B WHASH: {test8.compare_whash()}')
