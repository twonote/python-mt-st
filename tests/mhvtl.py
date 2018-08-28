# -*- coding: utf-8 -*-
import subprocess
import time

import tape_conf as conf


def reset():
    if conf.HIT_MHVTL:
        _reset()
    else:
        print("Not hit mhvtl. let all drive slots empty and all storage slots full by yourself")


def _reset():
    time.sleep(10)
    subprocess.run(["/etc/init.d/mhvtl", "shutdown"], timeout=10, check=True)
    time.sleep(10)
    subprocess.run(["/etc/init.d/mhvtl", "start"], timeout=10, check=True)
    time.sleep(3)
