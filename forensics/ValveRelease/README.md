# Valve Release

**Author:** unterd0g
**Category:** forensics / crypto
**Difficulty:** medium-hard

## Description

Hi,

We operate a humble sewage treatment plant and are now facing a severe emergency. Our city was hit hard by this ransomware attack, and we were no exception. Our technician knew about the attack in the city and realized something was wrong with the main workstation (way too much hard-drive activity), so he pulled the power plug quite fast. However, the system no longer boots, and sh%t is about to blow up (quite literally!).

We need to activate the emergency release valve. Please help us! We have attached an image of the system drive.

## Solve

The ransomware was encrypting that drive sequentially, from the beginning to the end. Pulling the power cord mid-way meant there was unencrypted data still salvageable.
There is no memory dump available or any other way to recover the malware's encryption key.

It turns out the cut-off point is in the middle of the private RSA key the valve release client uses to authenticate the emergency message. That client is also unencrypted and in the following bytes after the key (i.e., the files in the Ext4 FS were nearby).

The partial key is:
```
7k9gByKjip1Qau03ZIEHG4NCsuhAtLPa6wJAKOsORyBatM88ykaO9lz64ArV/Bll
a6lnZE816CJCDfhwOsPH4SbOMMEeBZiWvRkopIhgBX55TCMXiglcQGW2jwJBALLK
IkKm1ojvxAo57GjprKk90KgNsR2wjEwIGZZaA7jTFsS4qLxN6bC2I3rnlwc2rOHW
EjIk1u4RpAUL/pokT6MCQDmhS8OOQfZvgVIU31RLPaEL1VFJjcEXQb3+kHD8sFls
IV7lOS8VuoXQMdUNP1/Iio/6xjno+bIW3LmftNhPoT4=
-----END RSA PRIVATE KEY-----
```

(The client and all server-side sources are also available in our repository so that you may replicate the challenge locally)

Our expected path is to decode the PEM (and ASN.1 structure), recovering a partial q, dp, dq, and qinv.
It is easy to determine we have a 1024bit key by looking at the parameter lenghts. We expected you to assume the default e = 65537 (or 0x10001).

The challenge was devised so that you could recover the full key using [X].
You can also check our solver.py, but be warned the code there is not that pretty.

From thereafter, you may either rework the valve release python client to use the RSA key parameters or rebuild the secret.pem from those parameters.
Our solver follows the later approach. The server-side will send you the flag once you sign the emergency message correctly.

## Flag ##

CTFUA{8251219ca77c9a046374ebe5a839135b3cd450bd8db6641fcba4ce79de44c3c2}
