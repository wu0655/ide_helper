#!/usr/bin/python3
import os
import sys

from common.OutDirAnalyzer import OutDirAnalyzer
from common.file_parser.o_cmd_Parser import o_cmd_Parser
from common.file_parser.uboot_d_pre_tmp_Parser import uboot_d_pre_tmp_Parser


class UbootOutDirAnalyzer(OutDirAnalyzer):
    def init(self):
        code_files_db = []
        for root, dirs, files in os.walk(self.blt_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".o.cmd"):
                    parser = o_cmd_Parser(self.blt_dir, self.code_dir, filepath)
                    parser.parse()
                    code_files_db.append(parser.out())
        for root, dirs, files in os.walk(self.blt_dir + os.sep + "arch"):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".d.pre.tmp"):
                    parser = uboot_d_pre_tmp_Parser(self.blt_dir, self.code_dir, filepath)
                    parser.parse()
                    code_files_db.append(parser.out())
        self.merge_set(code_files_db)
        self.scan_auto_gen_h()


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 2:
        exit(0)

    _blt_dir = os.path.realpath(sys.argv[1])
    _src_dir = os.path.realpath(_blt_dir + os.sep + "source")
    shell_dir = sys.argv[2]

    obj = UbootOutDirAnalyzer(_blt_dir, shell_dir)
    obj.init()
    obj.output()
