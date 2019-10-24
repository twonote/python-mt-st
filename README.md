[![PyPI version](https://badge.fury.io/py/python-mt-st.svg)](https://pypi.org/project/python-mt-st/)

A magnetic tape drive controller ✨🍰✨
=======================================================

![Screenshot](https://user-images.githubusercontent.com/3183314/44708568-09def800-aada-11e8-9a2c-f576c9d8f00f.png)

A Python module for controlling magnetic tape drives under Linux. The module can perform tape drive operation, just like mt variants (mt-st, mt-gnu, etc.) under Unix-like OSs. For example, a user can rewind, forward/backward space, erase the cartridge, and so on. The current implementation is just a wrapper of mt-gnu. In the future, we will move to communicate with
Linux st driver directly via ioctl instead.


## Usage

[TODO]

## Prerequisites

1. Linux/Python 3
2. The current version is wrapping GNU tools. Make sure mt-gnu/mt-st/sg_logs is in your execution path.
3. Root privilege is necessary for operating a magnetic tape drive.
4. You will need either a real tape drive or use mhvtl as a simulate tape drive.

## Install

1. ``$ cd [project_home]``
2. ``$ pip install .``

## Tape Drive Configuration

1. You can find out what tape devices you 
have by this [guide](https://www.bacula.org/7.2.x-manuals/en/problems/Testing_Your_Tape_Drive_Wit.html#SECTION00423000000000000000).  
2. Ensuring that the tape modes are properly set by following commands: (Assume your tape drive is in /dev/nst0)
* mt -f /dev/nst0 stoptions buffer-writes async-writes read-ahead
* mt -f /dev/nst0 defblksize 0

## Testing 

1. You need either a real tape drive or [mhvtl](https://github.com/markh794/mhvtl) for simulation.
2. After tape drive is ready, update tape drive information in ```test/tape_conf.py```
3. run test cases by ```$ make test```
