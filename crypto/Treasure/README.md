# Treasure

**Author:** Dinis
**Category:** misc
**Difficulty:** Easy

## Description

It looks like a 5 years old drew this. Can you help the kid find the flag?

**Solve**

This challenge presents 2 files, a flag.txt and a map.png

This is a treasure hunt where it seems the map has the instructions on how to get the flag

The first step would be to xor the map with the flag.txt file

After finding out that A000045 represents the Fibonnaci sequence (https://oeis.org/A000045), the objective was to remove all bits from the Fibonnaci positions, so on the xor'd results we would take one the bit in position 1,1,2,3,5,8,11 ...

After this with the clue that A=41 all that was needed was to change the bits we had into ascii letters and we would get the flag

## Flag

CTFUA{eNcOdInG_iS_aMaZiNg}
