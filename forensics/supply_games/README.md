# Supply Games
**AUTHOR**
duarte; orang3

**CATEGORY**
forensics

**DIFFICULTY**
easy

**DESCRIPTION**
```
A class assignment was focused on developing a retro game. Our students created a Pacman, but we think they tried to trick us.
```

**SOLVE**
```
The pacman.py is a simple Pacman game made with python, which uses functions in the utils.py file and requires pip packages included in the requirements.txt.

Actually, it does not require all the packages included in the requirements.txt file. The majority of the requirements are useless and their only purpose is to offuscate the names of the packages that are actually used, more specifically the package "tutle", which is a typosquatting of the original Python package "Turtle". "tutle" was intentionally uploaded to pypi.org (the Python Package Index repository) by us, which does everything that "Turtle" does, plus something else.

Once you install "tutle" through pip and pacman.py uses it, you're running potentially malicious code without knowing, because we can upload whatever we want to PyPi :).

The tutle.py file used by the "tutle" package includes somewhere between two functions the following code:

import tempfile
temp = tempfile.NamedTemporaryFile(mode='wb', buffering=0)
temp.write(bytes.fromhex('43544655417b30485f4e6f215f705950495f48696a41636b217d'))

This code writes the flag to a file inside your temporary files folder (in UNIX, /tmp), while pacman.py is running. So when you were running the game trying to find the flag, it was written in that folder and accessible by you all along :).

This is harmless, but any block of code can be run in this situation, so pay attention to the pip packages that you install!
```

**FLAG**
```
CTFUA{0H_No!_pYPI_HijAck!}
```