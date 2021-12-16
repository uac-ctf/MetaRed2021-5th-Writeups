# Thief

**Author:** thiefCatcher
**Category:** rev
**Difficulty:** hard

## Description
```
We know that a student is trying to steal information from the university servers. Please help us to reverse the binary we found in the new apple server.

You must have one or the other but not both.
```

## Solve

This challenge can be solved following different approaches. We provided a binary file compiled using Nuitka in a MacOS with M1 process and using the clang compiler.
Since we used a python version hard to decompile, so the best approach is to try to look directly at the binary, or try to run the application and analyse the application behaviour. The goal of this binary is to exfiltrate information using DNS requests, and its implementation has a mode to test the service. 


<img width="829" alt="Captura de ecra" src="https://user-images.githubusercontent.com/17878072/146395889-aec463af-649b-45de-9788-addacdbd3b8d.png">


The test mode tries to exfiltrate 7 files that are the flag split into seven parts. These files do not need to exist.

A different way to access the names of these 7 files is by looking at the binary. Using strings command, we obtain the beginning of the flag "CTFUA{". 


<img width="394" alt="Captura de ecra2" src="https://user-images.githubusercontent.com/17878072/146397557-707c7be8-1936-4276-949c-d8935c900c99.png">


Using the xxd command and sending the output to a file, we can search for keywords. By searching for the word we found ("CTFUA{"), we obtain the following scenario.

![Captura de ecrã 2021-12-16, às 15 14 53](https://user-images.githubusercontent.com/17878072/146397982-3186426e-6920-4709-a183-058fee70eeb2.png)

In this analyse, we were able to identify the "FLAG_TEST", which is followed by something not usual in base32 `IZWGCZZANFZSA3TPOQQGS3RAORUGS4ZAOZQXE===`.

```
000ad240: 6143 5446 0061 464c 4147 5f54 4553 5400  aCTF.aFLAG_TEST.
000ad250: 5401 0000 0075 495a 5747 435a 5a41 4e46  T....uIZWGCZZANF
000ad260: 5a53 4133 5450 4f51 5147 5333 5241 4f52  ZSA3TPOQQGS3RAOR
000ad270: 5547 5334 5a41 4f5a 5158 453d 3d3d 0054  UGS4ZAOZQXE===.T
```

Using CyberChef, we can obtain the string "Flag is not in this var" (https://gchq.github.io/CyberChef/#recipe=From_Base32('A-Z2-7%3D',true)&input=SVpXR0NaWkFORlpTQTNUUE9RUUdTM1JBT1JVR1M0WkFPWlFYRT09PQ). However, there are more evidences of strings in base32 format.

```
000ad2b0: 6145 5534 434f 4d52 4800 7541 5a51 5859  aEU4COMRH.uAZQXY
000ad2c0: 4549 4b42 4546 5141 3d3d 3d00 7541 4251  EIKBEFQA===.uABQ
000ad2d0: 5159 4651 5744 5149 4257 3d3d 3d00 7542  QYFQWDQIBW===.uB
000ad2e0: 4d4b 4141 4541 5544 5541 4249 3d3d 3d00  MKAAEAUDUABI===.
000ad2f0: 7541 4e32 514d 4544 5443 4d4d 4134 3d3d  uAN2QMEDTCMMA4==
000ad300: 3d00 7542 5234 5153 4649 4343 3446 5232  =.uBR4QSFICC4FR2
000ad310: 3d3d 3d00 7544 513d 3d3d 3d3d 3d00 7549  ===.uDQ======.uI
```

The pieces of interest are: "EU4COMRH", "AZQXYEIKBEFQA===", "ABQQYFQWDQIBW===", "BMKAAEAUDUABI===", "AN2QMEDTCMMA4===", "BR4QSFICC4FR2===" and "DQ======".
Using CyberChef with the value "EU4COMRH" as input, and the recipes "From Base32" and "XOR" with the key CTFUA (which is the beginning of the flag) to obtain the "flagf" value. So, we need to keep "flag" as a key for future reference.
The next blocks were bigger than the first (except the last). These blocks were XOR with the block before, similar to CFB mode chipher.

```
"EU4COMRH"          -> "EU4COMRH"
"AZQXYEIKBEFQA==="  -> "C4HREDYH"
"ABQQYFQWDQIBW==="  -> "CUDDSXIS"
"BMKAAEAUDUABI==="  -> "HADTGEIG"
"AN2QMEDTCMMA4==="  -> "K4BD4VQI"
"BR4QSFICC4FR2==="  -> "GMKQ6AZT"
"DQ======"          -> "DQ======"
```

These pieces need to be concatenated, so you obtain the flag in base32 "EU4COMRHC4HREDYHCUDDSXISHADTGEIGK4BD4VQIGMKQ6AZTDQ======". To obtain the flag, just use the same 2 recipes in CyberChef  "From Base32" and "XOR" with the key "flag".

## Flag

CTFUA{nuikta_1s_a_pa1n_1n_the_}
