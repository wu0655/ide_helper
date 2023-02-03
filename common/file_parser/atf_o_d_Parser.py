#!/usr/bin/python3
import os
import sys

from common.file_parser.d_pre_tmp_Parser import d_pre_tmp_Parser

"""
atf dtb deps file
"""


class atf_o_d_Parser(d_pre_tmp_Parser):
    def to_abs_path(self, path):
        if path.startswith(os.sep):
            xpath = path.strip()
        else:
            xpath = self.code_dir + os.sep + path.strip()
        return os.path.abspath(xpath)


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    _blt = os.path.realpath("/home/wu/work/nxp/wr_atf/arm-trusted-firmware/build/fawcgw/release")
    _code = os.path.realpath("/home/wu/work/nxp/wr_atf/arm-trusted-firmware")
    _file = "./test_example/atf/fawcgw-v1-0.o.d"
    obj = atf_o_d_Parser(_blt, _code, _file)
    obj.parse()
    obj.dump()
