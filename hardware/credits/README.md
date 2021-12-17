# Credits

**Author:** rackham
**Category:** hardware
**Difficulty:** medium

## Description
```
We would like to _Display_ credit to all the UA Cyber Sec Team. Enjoy the CTF, Merry Christmas and take our modern paper card.

```


## Solve

A file named data.sr was provided, which could be open with `Pulseview`. The file is actually a `ZIP` and a `metadata` file would hint towards `sigrok`.

Opening the file with `pulseview` would result in a reasonable number of events across multiple pins.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/hardware/credits/pv1.png?raw=true)

Zooming in into each event would reveal a structure composed by an initial set of transactions, and then two chunks of data.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/hardware/credits/pv2.png?raw=true)

The description pointed towards a Display as the word was bold. This pattern is consistent with filling a frame buffer for a display.

Channel 6 also looks like a clock, while D5 looks like data. Spinning an SPI decoder to these channels would allow obtaining a stream of bits. These bits could correspond to RGB values in a color display, or direct values for a monochrome display. This was actually the case.

A proper solve would involve parsing the SPI messages. A quicker solve would imply creating an image with `PIL`. An even quicker solve would involve a oneliner.

If we saved one of the large chunks to a file named `buffer.txt`, by exporting the annotations of the D5 channel, we could use the following:

```cat buffer.txt |cut -d ' ' -f 5 |tr -d '\n' |tr -d '\r' |sed -e "s/.\{104\}/&\n/g" -e "s/1/ /g"```

The result would be:
```
                                                 000000
                                               0000000000
                                              0000    0000
                                              00        00
                                             000        000
                                             00          00
                                             00          00
                                             00          00
                                             000        000
                                              000      000
                                              0000    0000
                                               00      00

                                                         00
                                                         00
                                                         00
                                                         00
                                                         00
                                             00000000000000
                                             00000000000000
                                                         00
                                                         00
                                                         00
                                                         00



                                             00000000000000
                                             00000000000000
                                                   00    00
                                                   00    00
                                                   00    00
                                                   00    00
                                                   00    00
                                                   00    00
                                                   00    00
                                                         00

                                                  000000000
                                               000000000000
                                              0000000000000
                                             000
                                             000
                                             00
                                             00
                                             000
                                              0000
                                              0000000000000
                                                00000000000

                                             0
                                             0000
                                             000000
                                               0000000
                                                00000000
                                                00  0000000
                                                00     0000
                                                00   000000
                                                00000000
                                               0000000
                                             000000
                                             0000
                                             0

                                                  000
                                            0000000 0000000
                                           00000000 0000000
                                           00             00
                                           00             00

                                               00      0
                                              000      000
                                             000       0000
                                             00         000
                                             00    00    00
                                             00    00    00
                                             000   000  000
                                              000000000000
                                              000000 0000
                                                00



                                             00000000000000
                                             00000000000000
                                                   00    00
                                                   00    00
                                                   00    00
                                                   00   000
                                                   00000000
                                                    000000
                                                     0000
                                                00
                                                000
                                                00000
                                                000000
                                                00  000
                                                00   0000
                                                00     000
                                             00000000000000
                                             00000000000000
                                                00
                                                00


                                         00000000000000
                                         00000000000000
                                         00000000000000
                                              00    000
                                             00      00
                                             00      00
                                             000     00
                                             0000000000
                                              00000000
                                                0000

                                               00      0
                                              000      000
                                             000       0000
                                             00         000
                                             00    00    00
                                             00    00    00
                                             000   000  000
                                              000000000000
                                              000000 0000
                                                00


                                             0000000000
                                             0000000000
                                             0000000000
                                                    00
                                                     00
                                                     00
                                                     00


                                           00
                                           00
                                           00
                                           00
                                           00
                                           00
                                           00
                                           00


                                                      0
                                                  00000
                                               00000000
                                             0000000
                                             0000
                                              0000000
                                                 000000
                                                  00000
                                               0000000
                                             00000
                                             000000
                                              00000000
                                                 000000
                                                     00


                                           00
                                           00
                                           00
                                           00
                                           00
                                           00
                                           00
                                           00



                                               000  00
                                              0000  0000000
                                              000   0000000
                                             000    000  00
                                             00      00  00
                                             00      00  00
                                             000    000  00
                                              00000000   00
                                               000000    00
                                                0000



                                             00000000000000
                                             00000000000000
                                                   00    00
                                                   00    00
                                                   00    00
                                                   00   000
                                                   00000000
                                                    000000
                                                     0000


                                                       00
                                                       00
                                                       00
                                             0000000000000
                                             00000000000000
                                             00000000000000





                                           00             00
                                           0000000  0000000
                                            0000000 0000000

```


## Flag

CTFUA{3P4p3r_w_5P1}
