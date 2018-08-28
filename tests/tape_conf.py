# -*- coding: utf-8 -*-
import os

# Assumes hitting mhvtl simulated STK L80 medium changer
STK_L80_prop = {
    'mediumx': '/dev/tape/by-id/scsi-SSTK_L80_XYZZY_B',
    'device': '/dev/tape/by-id/scsi-350223344ab000900-nst',
    'first_data_slot_addr': 500,
    'first_storage_slot_addr': 1000,
    'first_storage_slot_cartridge': 'G03001TA',
}

HIT_MHVTL = True

if os.environ.get('HIT_MHVTL') == '0':
    HIT_MHVTL = False

print('HITMHVTL: ' + str(HIT_MHVTL))

"""
Enther first three members
"""
prop = {
    'mediumx': '',
    'device': '',
    'first_storage_slot_cartridge': '',
    'first_data_slot_addr': 0,
    'first_storage_slot_addr': 0,
}

if HIT_MHVTL:
    prop = STK_L80_prop
else:
    print('Make sure config prop by yourself')
