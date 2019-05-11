from PIL import Image
from math import sqrt

imgs_left = ["pieces/" + str(i)+".png" for i in range(0, 128)]

def distance(px1, px2):
    return sqrt((px2[0]-px1[0])**2 + (px2[1]-px1[1])**2 + (px2[2]-px1[2])**2)

def find_closest(px):
    min_distance = 1000
    closest_img = 0
    
    for img_path in imgs_left:
        with Image.open(img_path) as img:
            px1 = img.getpixel((10, 10))
            d = distance(px, px1)
            if d < min_distance:
                min_distance = d
                closest_img = img_path
    
    return closest_img

x_offset = 0
sum_width = 44 * 128
height = 224

res_im = Image.new("RGB", (sum_width, height))

closest_img = imgs_left[26]
imgs_left.remove(closest_img)

while len(imgs_left) > 0:
    with Image.open(closest_img) as img:
        res_im.paste(img, (x_offset, 0))
        x_offset += img.size[0]
        
        px = img.getpixel((img.size[0] - 10, 10))

        closest_img = find_closest(px)
        imgs_left.remove(closest_img)

res_im.save("flag.png")