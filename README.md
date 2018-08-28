A magnetic tape drive controller ✨🍰✨
=======================================================

![Screenshot](https://user-images.githubusercontent.com/3183314/44708568-09def800-aada-11e8-9a2c-f576c9d8f00f.png)

A Python module for controlling magnetic tape drives under Linux from Python. The module can control 
magnetic tape drive operation, just like mt variants (mt-st, mt-gnu, etc.) under Unix-like OSs.
User can do control operations and erase the cartridge. This implementation is based on
mt-gnu. In the next version we will move to communicate with linux st driver via ioctl instead.


## Usage

[TODO]

## Prerequisites

1. Current version is wrapping mt-gnu. Make sure mt-gnu is in your execution path.
2. root privilege needed by magnetic tape drive operations
3. Python 3


## Install

1. ``$ cd [project_home]``
2. ``$ pip install .``


## Testing 

1. You need either a real tape drive or use [mhvtl](https://github.com/markh794/mhvtl) as a simulate tape drive.
2. After tape drive is ready, update tape drive information in ```test/tape_conf.py```
3. run test cases by ```$ nosetests tests```
