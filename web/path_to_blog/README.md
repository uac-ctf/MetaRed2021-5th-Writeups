# ## Path to Blog (/)

**Author:** randN
**Category:** web
**Difficulty:** easy

## Description
```
A professor deployed his blog with a popular web server. But he forgot the path to the rest of the blog, help him find the path to the blog /.
```

## Solve

The challenges provide a simple web page, with nothing that useful. The source code does not have anything special, no links and different pages. But the response headers leak some information about the server and its version.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/path_to_blog/images/page_header.png?raw=true)

Doing a quick google search about vulnerabilities in Apache... <https://httpd.apache.org/security/vulnerabilities_24.html> So the version 2.4.50 is vulnerable to Path Traversal and Remote Code Exection (RCE). There are PoCs available that we can use to explore this vulnerability, we are going to use the one provided in [Exploit-DB](https://www.exploit-db.com/exploits/50406).

Let's test it out:

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/path_to_blog/images/whoami.png?raw=true)

Now we know that we can execute commands with the **daemon** user. Let's list the contents of the current dir, maybe we can find more useful information. There are two files that by the name of them must be the path that we should take to solve the challenge.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/path_to_blog/images/listing_current_dir.png?raw=true)

The **read_flag** binary has the setuid (and setgid) bit set, so we can run the executable with the same file permissions of the executable's owner (group). There is also the binary source code:

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/path_to_blog/images/read_flag.png?raw=true)

Looking into the code we can see that it gets the current user id and checks if it's equal to zero. If this condition is met we will be able to read the flag, and in order to do this we can explore a buffer overflow vulnerability when reading a string (**gets(input)**). A good example how to explore this problem, <https://0xrick.github.io/binary-exploitation/bof2/>.
To make it easy, let's write the payload to a file and then **cat** the contents of it to the **read_flag** binary.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/path_to_blog/images/flag.png?raw=true)

And we have the flag.

## Flag

CTFUA{P4th_n0rm4lize_g0n3_wRonG}
