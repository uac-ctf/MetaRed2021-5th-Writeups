# Happy meal

**Author:** thiefCatcher
**Category:** forensics
**Difficulty:** easy

## Description

The students did a lunch meeting at MacDonald's, but before they went to lunch, they push the new code to the repository.

## Solve

The bots.zip contains a git repository with a python script. This repository has 2 branches and it is necessary to switch between branches to see more commits and files. In the second branch, there is a .DS_Store file that contains the flag.

To see the flag, it is necessary to open the file in a hex editor/visualizer. For instance, the command xxd is enough.


## Flag

CTFUA{M4cOS_1s_n0t_4_me4l}