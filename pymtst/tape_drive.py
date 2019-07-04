# -*- coding: utf-8 -*-
import logging
import subprocess
from functools import wraps
from multiprocessing import Lock

logger = logging.getLogger(__name__)

# This table is based on "HPE StoreEver LTO-8 Ultrium Tape Drives Technical Reference Manual Volume 2 Software
# Integration Guide."
timeouts = {
    'status': 1 * 60,
    'rewind': 11 * 60,
    'eom': 49 * 60,
    'asf': 49 * 60,
    'weof': 28 * 60,
    'erase': 14.8 * 60 * 60,
}


def synchronized(tlockname):
    """A decorator to place an instance based lock around a method """

    def _synched(func):
        @wraps(func)
        def _synchronizer(self, *args, **kwargs):
            tlock = self.__getattribute__(tlockname)
            tlock.acquire()
            try:
                return func(self, *args, **kwargs)
            finally:
                tlock.release()

        return _synchronizer

    return _synched


class TapeDrive:
    """
    Class to represent a magnetic tape drive.

    User can do control operations and actually read/write/erase the cartridge. This implementation is based on
    mt-gnu and python tarfile.

    Note that user should only operate the drive this class represented to via this class simultaneously to prevent
    potential race conditions.

    """

    MT = 'mt-gnu'
    blocking_factor = 1024

    def __init__(self, device, self_check=False):
        """
         :param device: file name of the tape drive to operate on.

        """

        if not str(device).__contains__('n'):
            logger.warning("fool-proofing: it's not a good idea using rewind device here.")

        self.device = device

        if self_check:
            try:
                # fix mhvtl bug
                subprocess.run([self.MT, "-f", self.device, "rewind"], timeout=5, check=True, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, universal_newlines=True).stdout

                subprocess.run([self.MT, "-f", self.device, "status"], timeout=5, check=True, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, universal_newlines=True).stdout
            # Expect to raise another exception when the drive is busy or unexpected error occurred.
            except subprocess.TimeoutExpired:
                logger.error('Cannot check status... is the cartridge already loaded?')
                raise

        self._lock = Lock()

    def _execute_mt(self, args):
        """
        Execute mt-gnu command with the drive and args

         :param args: an array of mt's "operation, [count]"
         :raise subprocess exception with stderr

        """
        # TODO: wall clock
        logger.debug("pre-execute_mt:: args: '%s', timeout: '%d', file number: '%d'", str(args), timeouts.get(args[0]),
                     self.current_file_number())
        try:
            subprocess.run([self.MT, "-f", self.device] + args, timeout=timeouts.get(args[0]), check=True,
                           stderr=subprocess.PIPE)
        finally:
            logger.debug("post-execute_mt:: file number: '%d'", self.current_file_number())

    @synchronized('_lock')
    def status(self):
        return self._status()

    def _status(self):
        return subprocess.run([self.MT, "-f", self.device, "status"], timeout=timeouts.get("status"), check=True,
                              stderr=subprocess.PIPE,
                              stdout=subprocess.PIPE, universal_newlines=True).stdout

    @synchronized('_lock')
    def rewind(self):
        self._rewind()

    def _rewind(self):
        self._execute_mt(["rewind"])

    @synchronized('_lock')
    def eom(self):
        self._execute_mt(["eom"])

    @synchronized('_lock')
    def asf(self, count):
        self._execute_mt(["asf", str(count)])

    @synchronized('_lock')
    def erase(self, quickly=True):
        self._rewind()

        if quickly:
            self._execute_mt(["weof"])
        else:
            self._execute_mt(["erase"])

    def current_file_number(self):
        return self._parse_file_number(self._status())

    @staticmethod
    def _parse_file_number(status):
        for line in status.splitlines():
            if 'file number' in line:
                logger.debug('file number line: %s', line)
                return int(line.split('=')[1].strip())
        raise Exception('Cannot find file number in status.')
