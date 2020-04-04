
from PIL import Image, ImageDraw
from random import randint

def show():
    sz = 16
    bl = 16
    w = h = sz * bl

    im = Image.new("RGB", (w,h), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    for x in range(0,bl+1):
        for y in range(0,bl+1):
            p1 = (x-1) * bl
            p3 = (y-1) * bl
            p2 = x * bl * 2
            p4 = y * bl * 2

            draw.rectangle((p1,p3,p2,p4),
                fill=(int(x*bl/2), int(y*bl/2), 0)
                # fill=(
                #     randint(0, 256),
                #     randint(0, 256),
                #     randint(0, 256)
                # )
            )

    im.save( TEXTURE_PATH , "PNG")
