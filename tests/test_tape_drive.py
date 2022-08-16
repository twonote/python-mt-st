# -*- coding: utf-8 -*-
import subprocess
import time
from unittest import TestCase

from pymtst.tape_drive import TapeDrive
from tests import mhvtl
from tests import tape_conf

test_dir = "/tmp/test_drive"
prop = tape_conf.prop
TIMEOUT = 60 * 3


def prepare_tape():
    if tape_conf.HIT_MHVTL:
        mhvtl.reset()

    subprocess.run(['mtx', "-f", prop['mediumx'], "unload", "1", "0"], timeout=TIMEOUT, check=False)
    print('wait for unload...')
    time.sleep(1)  # mhvtl: unload is asynchronous

    subprocess.run(['mtx', "-f", prop['mediumx'], "load", "1", "0"], timeout=TIMEOUT, check=True)

    if tape_conf.HIT_MHVTL:
        # mhvtl bug mhvtl/issues/4
        subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)

    subprocess.run(['mt-gnu', "-f", prop['device'], "weof"], timeout=TIMEOUT, check=True)


class TestTapeDriveOffline(TestCase):
    d = None

    @classmethod
    def setUpClass(self):
        prepare_tape()
        self.d = TapeDrive(prop['device'])

    def test_offline(self):
        self.assertTrue(self.d.is_online())
        self.d.offline()
        self.assertFalse(self.d.is_online())


class TestTapeDrive(TestCase):
    d = None

    @classmethod
    def setUpClass(self):
        prepare_tape()
        self.d = TapeDrive(prop['device'])

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

    def test_fsf(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)
        self.d.fsf(1)
        self.assertEqual(1, self.d.current_file_number())

        subprocess.run(['mt-gnu', "-f", prop['device'], "eom"], timeout=TIMEOUT, check=True)

        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.d.fsf(1)

        self.assertIn("Input/output error", str(cm.exception.stderr))

    def test_bsfm(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "asf", "1"], timeout=TIMEOUT, check=True)

        self.d.bsfm(1)
        self.assertEqual(1, self.d.current_file_number())

        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.d.bsfm(2)

        self.assertIn("Input/output error", str(cm.exception.stderr))

    def test_erase(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "weof"], timeout=TIMEOUT, check=True)
        self.d.erase()
        subprocess.run(['mt-gnu', "-f", prop['device'], "eom"], timeout=TIMEOUT, check=True)
        self.assertEqual(1, self.d.current_file_number())

    def test_current_file_number(self):
        subprocess.run(['mt-gnu', "-f", prop['device'], "rewind"], timeout=TIMEOUT, check=True)
        self.assertEqual(0, self.d.current_file_number())
