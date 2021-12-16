# Tribute
**AUTHOR**

botto

**CATEGORY**

osint

**DIFFICULTY**

easy

**DESCRIPTION**
```
Our friend, known as the ghost in the wires,  finds his ways through the tactile pavings of the University of Aveiro. Can you help us find him on IG? He might be lost.
```

**SOLVE**
```
"known as the ghost in the wires" - leads to the name Kevin Mitnick

It's also known that the person is in the University of Aveiro.

The social media network is Instagram which is also given on the description.

Then the process to go to University of Aveiro followers' and search for Kevin Mitnick's account which is [this one](https://www.instagram.com/kv_mitnick/)

On the account there are multiple references that the account user is blind (not related to the real Kevin Mitnick).

On the first post in the account, the description gives a hint of the user hoping the photo can be described to them. 

Instagram allows to add alt-text to posts. This text can be read with a voice-over app that reads the screen content to the users. 

The flag was inserted in this post's alt-text. The objective is to listen to the flag being spelled.

Solutions included this method or the method of viewing Instagram's source code in which the flag is defined in the alt tag atribute of the image html tag. 

The flag was case insensitive since in the spelling method there is no way of telling which letters are upper or lower case.
```

**FLAG**
```
CTFUA{m0LiC3iR0}
```
