from PIL import Image

im_orig = Image.open("Bliss.bmp")
im_new = Image.open("bliss_new.bmp")

x = y = 0
result = ""

for x in range(0, im_new.size[0]):
    px_orig = im_orig.getpixel((x, y))
    px_new = im_new.getpixel((x, y))

    result += str(int(px_new != px_orig))

n = int(result, base=2)
print(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())