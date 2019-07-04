# -*- coding: utf-8 -*-
import subprocess
import time
from unittest import TestCase

from tests import mhvtl
from tests import tape_conf
from pymtst.tape_drive import TapeDrive

test_dir = "/tmp/test_drive"
prop = tape_conf.prop
TIMEOUT = 60 * 3


class TestTapeDrive(TestCase):
    d = None

    @classmethod
    def setUpClass(self):
        if tape_conf.HIT_MHVTL:
            mhvtl.reset()

        subprocess.run(['mtx', "-f", prop['mediumx'], "unload", "1", "0"], timeout=TIMEOUT, check=False)
        print('wait for unload...')
        time.sleep(1)  # mhvtl: unload is asynchronous

        subprocess.run(['mtx', "-f", prop['mediumx'], "load", "1", "0"], timeout=TIMEOUT, check=True)
        subprocess.run(['mt-gnu', "-f", prop['device'], "weof"], timeout=TIMEOUT, check=True)

        self.d = TapeDrive(prop['device'])

    # def setUp(self):
    #     subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)

    def test_status(self):
        self.assertIsNotNone(self.d.status())

    def test_rewind(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "eom"], timeout=TIMEOUT, check=True)
        self.d.rewind()
        self.assertEqual(0, self.d.current_file_number())

    def test_eom(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)
        self.d.eom()
        self.assertNotEqual(0, self.d.current_file_number())

    def test_asf(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)
        self.d.asf(1)
        self.assertEqual(1, self.d.current_file_number())

        subprocess.run(['mt-gnu', "-f", prop['device'], "eom"], timeout=TIMEOUT, check=True)
        self.d.asf(1)
        self.assertEqual(1, self.d.current_file_number())

        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.d.asf(999)

        self.assertIn("Input/output error", str(cm.exception.stderr))

    def test_erase(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "weof"], timeout=TIMEOUT, check=True)
        self.d.erase()
        subprocess.run(['mt-gnu', "-f", prop['device'], "eom"], timeout=TIMEOUT, check=True)
        self.assertEqual(1, self.d.current_file_number())

    def test_current_file_number(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)
        self.assertEqual(0, self.d.current_file_number())


def prepare_files():
    subprocess.run(["rm", "-rf", test_dir], timeout=TIMEOUT, check=True)

    subprocess.run(["mkdir", "-p", test_dir + '/to_migrated/files'], timeout=TIMEOUT, check=True)
    for i in range(3):
        subprocess.run(["truncate", "-s", "1M", test_dir + "/to_migrated/files/1M." + str(i)], timeout=TIMEOUT,
                       check=True)
