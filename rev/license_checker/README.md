# License Checker

**Author:** rackham
**Category:** rev
**Difficulty:** hard

## Description
```
If you have a valid license, you code can unlock the flag.

HINT: The binary may trick you and be picky, and then misbehave.

```


The challenge was a standard license checker where the player had to provide the valid license in order to obtain the flag. A file was provided with the binary file that was validating the code.

 ```
 License Checker
Enter License Key to get access
Format is: 0000-0000-0000-0000-0000-0000
>
```

It consisted in a standard reversing challenge, only with the detail that there were some simple features complicate decompilation just a little bit.

The core of the program was composed by 11 checks, and reversing the code in ghidra would yield a similar result.

```c
    result = check0(lkey, key_length);
    result |= check1(lkey, key_length);
    result |= check2(lkey, key_length);
    result |= check3(lkey, key_length);
    result |= check4(lkey, key_length);
    result |= check5(lkey, key_length);
    result |= check6(lkey, key_length);
    result |= check7(lkey, key_length);
    result |= check8(lkey, key_length);
    result |= check9(lkey, key_length);
    result |= check10(lkey, key_length);
    result |= check11(lkey, key_length);
```


Most of the checks were trivial as they consisted of a variable initialized at 0, some arithmetic and a return with a comparison to a constant. In order to succeed, all checks should return 0. Therefore you could just reverse one by one.

A typical check is:

```c
int FUN_00101323(long param_1)

{
  int iVar1;
  
  iVar1 = (int)*(undefined8 *)(param_1 + 0x10) * (int)*(undefined8 *)(param_1 + 0x50) +
          (int)*(undefined8 *)(param_1 + 0xe0) * (int)*(undefined8 *)(param_1 + 0x58) +
          (int)*(undefined8 *)(param_1 + 0x90) * (int)*(undefined8 *)(param_1 + 0x60) +
          (int)*(undefined8 *)(param_1 + 0xc8) * (int)*(undefined8 *)(param_1 + 0x68) + -0x461b;
  if (iVar1 < 0x1) {
    iVar1 = -iVar1;
  }
  return iVar1;
}

```


After some simple renaming and retyping, the function is simple to analyze.

```c
int FUN_00101323(long *buf)

{
  int result;
  
  result = (int)buf[0x2] * (int)buf[0xa] + (int)buf[0x1c] * (int)buf[0xb] +
           (int)buf[0x12] * (int)buf[0xc] + (int)buf[0x19] * (int)buf[0xd] + -0x461b;
  if (result < 0x1) {
    result = -result;
  }
  return result;
}
```


In `check7` the result was initialized as the value of `result = ptrace(PTRACE_TRACEME,0x0,0x1,0x0);`. This would yield a different value if `gdb` was used.


`check8` tries to get the value of `LD_PRELOAD` from the environment: `result = getenv("LD_PRELOAD");`.

`check11` is a little more complex as it has opaque predicates with bogus code, also with invalid opcodes.

The result is:

```
/* WARNING: Control flow encountered bad instruction data */

ulong check11(char *key,uint length)

{
  long lVar1;
  uint i;
  ulonglong result;
  
  result = 0x0;
  i = 0x0;
  while( true ) {
    if (length <= i) {
      return (ulong)((int)result - 0x19da1);
    }
    result = result + *(long *)(key + (ulong)((i * 0x25) % length) * 0x8) *
                      *(long *)(key + (ulong)((i * 0x15) % length) * 0x8);
    if (result == -*(long *)(key + 0x68)) {
      result = 0x101970;
      func_0x17d08521();
    }
    if (*(long *)(key + 0x20) == -*(long *)(key + 0x48)) {
                    /* WARNING: Bad instruction - Truncating control flow here */
      halt_baddata();
    }
    lVar1 = *(long *)(key + (ulong)((i * 0x4b) % length) * 0x8);
    if (*(long *)(key + 0x18) * 0x8d < *(long *)(key + 0xa8)) {
      *(int *)(lVar1 + 0x6b) = (int)register0x00000020 + -0x8;
      *(undefined *)(lVar1 + 0x6b) = *(undefined *)(lVar1 + 0x6b);
                    /* WARNING: Bad instruction - Truncating control flow here */
      halt_baddata();
    }
    result = result + *(long *)(key + (ulong)((i * 0x2b) % length) * 0x8) *
                      *(long *)(key + (ulong)((i * 0x17) % length) * 0x8) +
             *(long *)(key + (ulong)((i * 0x47) % length) * 0x8) * lVar1 +
             *(long *)(key + (ulong)((i * 0x59) % length) * 0x8) *
             *(long *)(key + (ulong)((i * 0x61) % length) * 0x8);
    if ((long)*(ulong *)(key + 0x60) < *(long *)(key + 0xe0) / 0x14) break;
    i = i + 0x5;
  }
  return *(ulong *)(key + 0x60);
}

```

The function has some arithmetic, but also conditions and even Bad instruction which prevent correct decompilation. One approach would be to analyze the remaining code and ignore the bogus code. Also, some patching of this bogus code with `NOP` would allow the decompiler to produce a nice decompilation.

```c

int check11(char *key,uint length)

{
  uint i;
  ulonglong result;
  
  result = 0x0;
  for (i = 0x0; i < length; i = i + 0x5) {
    result = result + *(long *)(key + (ulong)((i * 0x25) % length) * 0x8) *
                      *(long *)(key + (ulong)((i * 0x15) % length) * 0x8) +
             *(long *)(key + (ulong)((i * 0x2b) % length) * 0x8) *
             *(long *)(key + (ulong)((i * 0x17) % length) * 0x8) +
             *(long *)(key + (ulong)((i * 0x47) % length) * 0x8) *
             *(long *)(key + (ulong)((i * 0x4b) % length) * 0x8) +
             *(long *)(key + (ulong)((i * 0x59) % length) * 0x8) *
             *(long *)(key + (ulong)((i * 0x61) % length) * 0x8);
  }
  return (int)result + -0x19da1;
}

```python

After all conditions were obtained, it was only required to create a solver and set the correct conditions:
```for i in range(0, 29):
    s.add(Or(key[i] >= ord('0'), key[i] == ord('-')))
    s.add(key[i] <= ord('Z'))
    s.add(key[i] != ord(':'))
    s.add(key[i] != ord(';'))
    s.add(key[i] != ord('<'))
    s.add(key[i] != ord('='))
    s.add(key[i] != ord('>'))
    s.add(key[i] != ord('?'))
    s.add(key[i] != ord('@'))

# 0

s.add(key[4] == ord('-'))
s.add(key[9] == ord('-'))
s.add(key[14] == ord('-'))
s.add(key[19] == ord('-'))
s.add(key[24] == ord('-'))

# 1
s.add(key[0] == ord('U'))
s.add(key[1] == ord('A'))
s.add(key[2] == ord('V'))
s.add(key[3] == ord('R'))

# 2
s.add((key[5] + key[8] + key[6] + key[3] + key[7] + key[17] + key[8] + key[15]) == 475)

# 3
s.add((key[10] * key[2] + key[11] * key[28] + key[12] * key[18] + key[13] * key[25]) == 17947)

# 4
s.add((key[15] ^ key[23]) + (key[16] ^ key[16]) + (key[17] ^ key[10]) + (key[18] ^ key[1]) == 128)

# 5
s.add(((key[20] >> 3)  * key[11] + (key[21] << 5)  * key[12] + (key[22] >> 2)  * key[23] + (key[23] >> 4)  * key[27]) == 109434)

# 6
s.add((key[25] * 9 ) > key[10] * 3)
s.add((key[26] * 8)  < key[27] * 10)
s.add((key[27] * 130) > key[13] * 25)
s.add((key[28] * 20)  > key[16] * 9)

# 7
s.add( key[10] * (key[28] + key[17]) + (key[25] + ((key[3]) * key[23])  << 16) == 288566177)

#8
s.add((key[11] + 1) * key[18] * (key[8] - key[27]) + (key[13] - ((key[6]) * key[17])  << 4) == -201664)

# 9
s.add(
    ((key[3] << 7) - key[1])   +
    ((key[9] << 7) - key[4])   +
    ((key[15] << 7) - key[7])  +
    ((key[21] << 7) - key[10]) +
    ((key[27] << 7) - key[13])
    == 42066
)

# 10
s.add(key[0] != ord('-'))
s.add(key[1] != ord('-'))
s.add(key[2] != ord('-'))
s.add(key[3] != ord('-'))
s.add(key[5] != ord('-'))
s.add(key[6] != ord('-'))
s.add(key[7] != ord('-'))
s.add(key[8] != ord('-'))
s.add(key[10] != ord('-'))
s.add(key[11] != ord('-'))
s.add(key[12] != ord('-'))
s.add(key[13] != ord('-'))
s.add(key[15] != ord('-'))
s.add(key[16] != ord('-'))
s.add(key[17] != ord('-'))
s.add(key[18] != ord('-'))
s.add(key[20] != ord('-'))
s.add(key[21] != ord('-'))
s.add(key[22] != ord('-'))
s.add(key[23] != ord('-'))
s.add(key[25] != ord('-'))
s.add(key[26] != ord('-'))
s.add(key[27] != ord('-'))
s.add(key[28] != ord('-'))

# 11
s.add(
      key[0] * key[0] +
      key[0] * key[0] +
      key[0] * key[0] +
      key[0] * key[0] +
      key[18] * key[11] +
      key[28] * key[12] +
      key[27] * key[7] +
      key[21] * key[10] +
      key[7] * key[22] +
      key[27] * key[24] +
      key[25] * key[14] +
      key[13] * key[20] +
      key[25] * key[4] +
      key[26] * key[7] +
      key[23] * key[21] +
      key[5] * key[1] +
      key[14] * key[15] +
      key[25] * key[19] +
      key[21] * key[28] +
      key[26] * key[11] +
      key[3] * key[26] +
      key[24] * key[2] +
      key[19] * key[6] +
      key[18] * key[21] == 105889)
```

This would produce a license such as: `UAVR-55D0-IM33-4HG0-EBB5-9AVR`

If the license was provided, the checker would give the flag.

```
License Checker
Enter License Key to get access
Format is: 0000-0000-0000-0000-0000-0000
> UAVR-55D0-IM33-4HG0-EBB5-9AVR
License valid!
Content unlocked: CTFUA{H3ll0_f3ll0w_r3v3rs3r}
```


## Flag

CTFUA{H3ll0_f3ll0w_r3v3rs3r}
