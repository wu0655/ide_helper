#!/usr/bin/python3
import os
import sys

from common.FileType import FileType

"""
based on kernel *.d.pre.tmp
"""


class d_pre_tmp_Parser(object):
    # path
    file_path = ""
    blt_dir = ""
    code_dir = ""
    # result from .o.cmd file
    deps = set()
    target = ""
    # result after post parse
    out_dict = {}

    def __init__(self, blt, code, path):
        self.file_path = path
        self.blt_dir = blt
        self.code_dir = code

    def parse(self):
        self.parse_file()
        self.handle_deps()
        self.handle_target()

    def out(self):
        return self.out_dict

    def parse_file(self):
        whole = ""
        with open(self.file_path, 'r') as f:
            for line in f.readlines():
                x = line.strip()
                whole += x
                if x.endswith("\\"):
                    whole = whole[0:-1] + " "
                else:
                    whole = whole + " "

        str_array = whole.split(":")
        self.target = str_array[0].strip()
        tmp = str_array[1].strip().split(" ")
        for tt in tmp:
            t = tt.strip()
            if len(t) == 0:
                continue
            if t.endswith(".h") or t.endswith(".c") or t.endswith(".dtsi") or t.endswith(".dts"):
                self.deps.add(t)
            else:
                self.out_dict[t] = FileType.Other

    def handle_target(self):
        pass

    def handle_deps(self):
        for item in self.deps:
            # handle $(wildcard xxx)
            # TODO multi-file in one file.
            it = item.strip()
            if it.startswith("$(wildcard"):
                self.out_dict[it] = FileType.Wildcard
                continue

            # multi file in one, so split first
            for _tmp in it.split(" "):
                tmp = _tmp.strip()
                if len(tmp) == 0:
                    continue
                else:
                    key = self.to_abs_path(tmp)
                    if os.path.exists(key):
                        self.add_path_to_dict(self.out_dict, key)
                    else:
                        print("parse_deps file=" + self.file_path)
                        print("line=" + tmp)
                        print("key=" + key)

    def add_path_to_dict(self, d, in_path):
        path = self.to_abs_path(in_path)
        if path.startswith(self.blt_dir) or path.startswith(self.code_dir):
            d[path] = FileType.Code
        elif len(path) > 0:
            d[path] = FileType.Other

    def to_abs_path(self, path):
        if path.startswith(os.sep):
            xpath = path.strip()
        else:
            xpath = self.blt_dir + os.sep + path.strip()
        return os.path.abspath(xpath)

    def dump(self):
        print("-------dir----------")
        print("blt_dir=", self.blt_dir)
        print("code_dir=", self.code_dir)
        print("file_path=", self.file_path)
        print("-------deps----------")
        for val in self.deps:
            print(val)
        print("-------out_dict----------")
        sorted_list = sorted(self.out_dict.items(), key=lambda x: x[1])
        for item in sorted_list:
            print(item)


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    _blt = os.path.realpath("/home/wu/work/nxp/wr_atf/kernel/out/")
    _code = os.path.realpath("/home/wu/work/nxp/wr_atf/kernel/out/source")
    _file = "./test_example/kernel/.batman-v1-0.dtb.d.pre.tmp"
    obj = d_pre_tmp_Parser(_blt, _code, _file)
    obj.parse()
    obj.dump()
