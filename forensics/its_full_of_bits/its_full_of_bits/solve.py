from PIL import Image
import numpy as np

width = 512
height= 384

out = np.zeros([height, width, 3], dtype=np.uint8)
prev = 0

for i in range(256):
    print(i)
    with open(f'{i}.png', 'rb') as f:
        img = Image.open(f'{i}.png')
        
        array = np.array(img)
        if i != 0:
            for y in range(height):
                for x in range(width):
                    if array[y][x][0] != prev[y][x][0]:
                        out[y][x][0]+=1
                    if array[y][x][1] != prev[y][x][1]:
                        out[y][x][1]+=1
                    if array[y][x][2] != prev[y][x][2]:
                        out[y][x][2]+=1
        prev = np.copy(array)


img = Image.fromarray(out)
img.save(f'out-{i}.png')

