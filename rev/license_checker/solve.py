from z3 import *
from pwn import *
    
s =  Solver()
key = [ BitVec('b%i' % i, 32) for i in range(0, 29) ]

for i in range(0, 29):
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

r = s.check()
print(r)

if r != unsat:
    mod = s.model()
    key_plain = ""
    log.success("Equation solved")
    for i in range(29):
        x = mod[key[i]].as_long()
        key_plain += chr(x)
    print(key_plain)
