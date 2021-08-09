## from PIL import Image
from PIL import Image
import os.path, sys


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop(path, dirs):
    for item in dirs:
        fullpath = os.path.join(path,item)         #corrected
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            imCrop = crop_center(im, 160, 160)
            imCrop.save(f + 'square.png', "PNG", quality=100)

if __name__ == '__main__':
    path = "audiochunks"
    dirs = os.listdir(path)
    crop(path, dirs)