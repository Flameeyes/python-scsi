# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI Write12 command and definitions
#


class Write12(SCSICommand):
    """
    A class to send a Write(12) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'wrprotect': [0xe0, 1],
                 'dpo': [0x10, 1],
                 'fua': [0x08, 1],
                 'lba': [0xffffffff, 2],
                 'group': [0x1f, 10],
                 'tl': [0xffffffff, 6], }

    def __init__(self,
                 opcode,
                 blocksize,
                 lba,
                 tl,
                 data,
                 wrprotect=0,
                 dpo=0,
                 fua=0,
                 group=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param blocksize: a blocksize
        :param lba: Logical Block Address
        :param tl: transfer length
        :param data: a byte array with data
        :param wrprotect=0:
        :param dpo=0:
        :param fua=0:
        :param group=0:
        """
        if blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self,
                             opcode,
                             blocksize * tl,
                             0)
        self.dataout = data
        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  lba=lba,
                                  tl=tl,
                                  wrprotect=wrprotect,
                                  dpo=dpo,
                                  fua=fua,
                                  group=group)
