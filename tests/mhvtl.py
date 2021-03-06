# -*- coding: utf-8 -*-
import subprocess
import time

from tests import tape_conf as conf


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
    # /dev/tape/by-id/* may not generated by udev after restart mhvtl on my machine. Trigger it manually.
    subprocess.run(["udevadm", "trigger"], timeout=10, check=True)
    time.sleep(1)



TIMEOUT = 60 * 3


def unload(device, slotnum: int, drivenum: int, timout=TIMEOUT):
    subprocess.run(['mtx', "-f", device, "unload", str(slotnum), str(drivenum)], timeout=TIMEOUT,
                   check=False)
    print('wait for unload...')
    time.sleep(1)  # mhvtl: unload is asynchronous