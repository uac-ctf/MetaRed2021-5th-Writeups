# Mutant Fly

**Author:** thiefCatcher
**Category:** misc
**Difficulty:** easy

## Description

One student of the Cybersecurity course was bitten by a fly and got strangely sick.
We need your help to find the mutated ACGT sequence, before we end up with a Flyman.
Hurry up... please.


## Solve

The challenge is a FASTQ file. This format is used for DNA and each read (DNA sequence) uses 4 lines:

	1. The read ID
	2. DNA
	3. Nothing important
	4. Quality scores

You can solve this using two approaches: 1) identify the read with higher quality scores (everything as I); or 2) getting all DNA sequences and encode them. The encoding map of the ACGT is the following:

	- "A":"00"
	- "C":"01"
	- "G":"10"
	- "T":"11"
  
Then, convert the binary to ASCII.

The read with higher quality scores is the following:
```
CAATCCCACACGCCCCCAACCTGTCGCCCGTGCGATATAACGTGCGCAATACCGTGCGCTCCTTCGTCATAACTAGCGCCCCTTCTCACGGAATCACGTGCCTTCGCACGTGATCACTTC
```

The binary representation of this read using this mapping is the following:
```
010000110101010001000110010101010100000101111011011001010110111001100011001100000110111001100100001100010110111001100111010111110110110100110000011100100110010101011111011101000110100000110100011011100101111101100100011011100011010001111101
```

## Flag

CTFUA{enc0nd1ng_m0re_th4n_dn4}
