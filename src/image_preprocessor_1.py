from PIL import Image
import imagehash

hash1 = imagehash.average_hash(Image.open('src/sound_images/sound1.png'))
hash2 = imagehash.average_hash(Image.open('src/sound_images/sound2.png'))
hash3 = imagehash.average_hash(Image.open('src/sound_images/sound3.png'))
hash4 = imagehash.average_hash(Image.open('src/sound_images/sound4.png'))

print(hash1 == hash1)

print(hash1 - hash2)
print(hash2 - hash1)

print(hash1 - hash3)
print(hash1 - hash4)