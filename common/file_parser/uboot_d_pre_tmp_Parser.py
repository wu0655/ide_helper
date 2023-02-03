#!/usr/bin/python3
import os
import sys

from common.file_parser.d_pre_tmp_Parser import d_pre_tmp_Parser


class uboot_d_pre_tmp_Parser(d_pre_tmp_Parser):
    def handle_target(self):
        # .fsl-s32g274aevb.dtb.d.pre.tmp
        s = self.target.split(".")
        dts_file = self.code_dir + os.sep + "arch/arm/dts/" + s[1].strip() + ".dts"
        self.add_path_to_dict(self.out_dict, dts_file)


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    _blt = os.path.realpath("/home/wu/work/nxp/wr_atf/u-boot/out/")
    _code = os.path.realpath("/home/wu/work/nxp/wr_atf/u-boot/out/source")
    _file = "./test_example/uboot/.hirain-s32g274a-fawcgw.dtb.d.pre.tmp"
    obj = uboot_d_pre_tmp_Parser(_blt, _code, _file)
    obj.parse()
    obj.dump()
