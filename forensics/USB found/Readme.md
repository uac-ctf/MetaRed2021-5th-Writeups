# USB found

**Author:** Unterd0g
**Category:** forensics
**Difficulty:** hard (meant to be one of the hardest in the CTF)

## Description ##

We have finally brought down the ringleader of a major cybercrimes operation that was causing all sorts of havoc throughout Europe. Word on the street is that a new attack is already underway, but the subject remains uncooperative. We have raided various locations and uncovered this USB pen drive and a Yubikey device. The drive was hidden deep into a well, and the Yubikey was in the house foundations.
We have immediately imaged the USB drive (see file attached). We will send you the Yubikey later for further examination. However, our agents already played with it and determined the Yubikey was configured so that short pressing the logo yielded one string, while long-pressing yielded another string. We have also attached the output of both presses (i.e., Yubikey slots).

Will this be enough to find the target?
(hint: the flag is hidden in the target file and has the usual format CTFUA{…})


## Solve ##

Open the first image in a loop device and mount the NTFS file system. Then, you'll need to open the next virtual drive with LUKS using one of the slots. A quick examination will reveal an ext4 filesystem full of kitten images. Ignore them. You'll need to recover a deleted file from that filesystem. The recovered file is a Veracrypt volume which you can open using the other slot. Now you'll see an image with the target. Veracrypt allows for hidden volumes, but that is not the path. The right path is to examine the image and then use steghide to reveal the flag (the key is both slots appended together -- which makes sense when operating an Yubikey configured this way).


## Flag ##

CTFUA{e38b16b0a3a1376175acf5240e48462f9587e3d26901bf972d7376fdde93b59f}
