# ## Authentication hardening

**Author:** randN
**Category:** web
**Difficulty:** medium

## Description
```
The students are planning a Christmas party. They contacted a catering service but they did not resist exploring some vulnerabilities in the company's site. They found that pizzas with union and cheese were in flash sales.
```

## Solve

We are presented with a page with some menu hyperlinks. The only ones that take us to different pages are the register and login, where we are allowed to create an account and login in with that account.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/authentication_hardening/images/register.png?raw=true)

After a successful login, if we look into the page source code there is a hyperlink tag that is commented out.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/authentication_hardening/images/admin_comment.png?raw=true)

If we try to access the admin page, we are presented with a **Forbidden**. Looking more carefully around there is also an image that does not load, but has some base64 content.

```html
<img src="data:image/png;base64, U2Vjb25kIGZhbGxlbiBvcmRlcgo=" class="w3-round w3-image w3-opacity-min" alt="Menu" style="width:100%">
```

Decoding the content, the result is **Second fallen order**. This will be useful. A new cookie is also given, **token**, that store a jwt.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/authentication_hardening/images/cookies.png?raw=true)

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/authentication_hardening/images/jwt.png?raw=true)

Looking at the headers of the jwt provided, there is the kid parameter, an optional header claim which holds a key identifier, that corresponds to the username that we provided when registering an account. Looking for vulnerabilities in jwt, more specifically in the kid parameter, https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens#kid-issues. Hmm, this looks interesting, there is a SQL injection issue, and with the hint **Second fallen order** we can assume that there is a [Second order SQLi](https://infosecwriteups.com/the-wrath-of-second-order-sql-injection-c9338a51c6d) vulnerability, also the challenge description has the **'union'** word in it. Let's create a new account, and in the username we are going to insert an SQLi payload, `' UNION SELECT 'key` and see if we can control the key used to sign/verify the jwt.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/authentication_hardening/images/register_sqli.png?raw=true)

Visiting the **admin** page an _Internal server error_ occurs, so we must be on the right track. Since we control the key now, we just need to forge a jwt where the **admin** claim is defined as true.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/authentication_hardening/images/forged_jwt.png?raw=true)

Now we just need to use the this jwt and access the **admin** page.

## Flag
CTFUA{Sec0nd_jWt_0rd3r_RlRXCg==}
