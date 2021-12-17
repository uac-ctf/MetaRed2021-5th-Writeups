from PIL import Image
import numpy as np
import random
import json
import os
import pickle

def encode(plane, x, y, px):
    r =  random.sample(range(0, 255), px[0])
    g =  random.sample(range(0, 255), px[1])
    b =  random.sample(range(0, 255), px[2])

    plane[y][x] = (r.sort(),g.sort(),b.sort())

src = Image.open('ua_sunset.bmp')
width, height = src.size
src_arr = np.array(src)

planes = [0]*height

if not os.path.exists('planes.json'):
    for y in range(height):
        if planes[y] == 0:
            planes[y] = [[0,0,0]]*width
        for x in range(width):
            px = src_arr[y][x]
            planes[y][x] = [random.sample(range(0, 255), px[0]),
                            random.sample(range(0, 255), px[1]),
                            random.sample(range(0, 255), px[2])]

    with open('planes.json', 'wb') as f:
        pickle.dump(planes, f, protocol=pickle.HIGHEST_PROTOCOL)

else:
    with open('planes.json', 'rb') as f:
        planes = pickle.load(f)

new_arr = np.zeros([src.size[1], src.size[0], 3], dtype=np.uint8)
for y in range(height):
    for x in range(width):
        new_arr[y][x][0] = random.randint(1, 255)
        new_arr[y][x][1] = random.randint(1, 255)
        new_arr[y][x][2] = random.randint(1, 255)

i = 0
while i < 256:
    print(f"Dumping: {i}")

    for y in range(height):
        for x in range(width):
            r = planes[y][x][0]
            g = planes[y][x][1]
            b = planes[y][x][2]

            if i in r:
                new_arr[y][x][0]  = random.randint(1, 255)
            if i in g:
                new_arr[y][x][1] = random.randint(1, 255)
            if i in b:
                new_arr[y][x][2]  = random.randint(1, 255)


    print(f"Saving {i}.png")
    new = Image.fromarray(new_arr)
    new.save(f"{i}.png")
    i+=1
