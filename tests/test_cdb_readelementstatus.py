#!/usr/bin/env python
# coding: utf-8
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.pyscsi import scsi_enum_readelementstatus as READELEMENTSTATUS
from pyscsi.pyscsi.scsi_cdb_readelementstatus import ReadElementStatus
from .mock_device import MockDevice, MockSCSI


def main():

    with MockSCSI(MockDevice(smc)) as s:
        # cdb for SMC: ReadElementStatus
        r = s.readelementstatus(300, 700, element_type=READELEMENTSTATUS.ELEMENT_TYPE.STORAGE, voltag=1, curdata=1, dvcid=1)
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.READ_ELEMENT_STATUS.value
        assert cdb[1] == 0x10 | READELEMENTSTATUS.ELEMENT_TYPE.STORAGE
        assert scsi_ba_to_int(cdb[2:4]) == 300
        assert scsi_ba_to_int(cdb[4:6]) == 700
        assert cdb[6] == 0x03
        assert scsi_ba_to_int(cdb[7:10]) == 16384
        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.READ_ELEMENT_STATUS.value
        assert cdb['voltag'] == 1
        assert cdb['element_type'] == READELEMENTSTATUS.ELEMENT_TYPE.STORAGE
        assert cdb['starting_element_address'] == 300
        assert cdb['num_elements'] == 700
        assert cdb['curdata'] == 1
        assert cdb['dvcid'] == 1
        assert cdb['alloc_len'] == 16384

        d = ReadElementStatus.unmarshall_cdb(ReadElementStatus.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()

