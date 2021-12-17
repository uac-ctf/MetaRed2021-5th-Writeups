# ## Its full of bits

**Author:** rackham
**Category:** forensics
**Difficulty:** medium

## Description
```
You know chaos and order? The trick is keep the balance.

```

## Solve

The challenge provided 256 images of aparent random noise. The description pointed towards chaos and order: entropy. Of course, it seemed like there was lots of entropy envolved.

![Example image](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/forensics/its_full_of_bits/0.png?raw=true)

In reality, the images were created by encoding the RGB value in the amount of entropy (number of changes) among that pixel in all images. If a given channel pixel changed it's value 42 times among the different image, the final image should have a pixel with that value.

In order to solve this challenge, several approaches could be followed. 

The simplest one was to XOR some random images. The result was a noise image with the flag on the bottom.

The full solve would recover the full image by processing all images.

We include both the challenge creator and the solver. The creator takes a base image and creates 256 images, while the solver recovers the original image.

![Final image](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/forensics/its_full_of_bits/ua_sunset.bmp?raw=true)


### FLAG

ctfua{3nj0y_th3_5un37}
