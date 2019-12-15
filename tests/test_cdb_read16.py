#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_cdb_read16 import Read16
from mock_device import MockDevice, MockSCSI


def main():

    with MockSCSI(MockDevice(sbc)) as s:
        s.blocksize = 512

        r = s.read16(1024, 27)
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.READ_16.value
        assert cdb[1] == 0
        assert scsi_ba_to_int(cdb[2:10]) == 1024
        assert scsi_ba_to_int(cdb[10:14]) == 27
        assert cdb[14] == 0
        assert cdb[15] == 0
        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.READ_16.value
        assert cdb['rdprotect'] == 0
        assert cdb['dpo'] == 0
        assert cdb['fua'] == 0
        assert cdb['rarc'] == 0
        assert cdb['lba'] == 1024
        assert cdb['group'] == 0
        assert cdb['tl'] == 27

        d = Read16.unmarshall_cdb(Read16.marshall_cdb(cdb))
        assert d == cdb

        r = s.read16(1024, 27, rdprotect=2, dpo=1, fua=1, rarc=1, group=19)
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.READ_16.value
        assert cdb[1] == 0x5c
        assert scsi_ba_to_int(cdb[2:10]) == 1024
        assert scsi_ba_to_int(cdb[10:14]) == 27
        assert cdb[14] == 0x13
        assert cdb[15] == 0
        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.READ_16.value
        assert cdb['rdprotect'] == 2
        assert cdb['dpo'] == 1
        assert cdb['fua'] == 1
        assert cdb['rarc'] == 1
        assert cdb['lba'] == 1024
        assert cdb['group'] == 19
        assert cdb['tl'] == 27

        d = Read16.unmarshall_cdb(Read16.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()

