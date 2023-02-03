#!/usr/bin/python3
import os
import sys

from common.FileType import FileType

"""
based on kernel *.o.cmd
"""


class atf_d_Parser(object):
    # path
    file_path = ""
    blt_dir = ""
    code_dir = ""
    # result from .o.cmd file
    source = set()
    deps = set()
    # result after post parse
    out_dict = {}

    def __init__(self, blt, code, path):
        self.file_path = path
        self.blt_dir = blt
        self.code_dir = code

    def parse(self):
        self.parse_file()
        self.post_parse()

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

        _mm_item = whole.split(":")
        for _m_item in _mm_item:
            _item = _m_item.strip().split(" ")
            for _key in _item:
                key = _key.strip()
                if key.endswith(".h") or key.endswith(".c") or key.endswith(".S") or key.endswith(".s"):
                    self.deps.add(key)
                elif key.endswith(".o"):
                    pass
                else:
                    self.out_dict[key] = FileType.Other

    def post_parse(self):
        if len(self.deps) > 0:
            self.handle_deps()
        if len(self.source) > 0:
            self.handle_source()

    def handle_source(self):
        for item in self.source:
            key = self.to_abs_path(item.strip())
            if os.path.exists(key):
                self.add_path_to_dict(self.out_dict, key)
            else:
                print("parse_source file=" + item)
                print("line=" + key)

    def handle_deps(self):
        for item in self.deps:
            # handle $(wildcard xxx)
            # TODO multi-file in one file.
            it = item.strip()
            if it.startswith("$(wildcard"):
                self.out_dict[it] = FileType.Wildcard
                continue

            # multi file in one, so split first
            for y1 in it.split(" "):
                i = y1.strip()
                if len(i) == 0:
                    continue
                else:
                    key = self.to_abs_path(i)
                    if os.path.exists(key):
                        self.add_path_to_dict(self.out_dict, key)
                    else:
                        print("parse_deps file=" + self.file_path)
                        print("line=" + key)

    def add_path_to_dict(self, d, in_path):
        path = self.to_abs_path(in_path)
        if path.startswith(self.blt_dir) or path.startswith(self.code_dir):
            d[path] = FileType.Code
        else:
            d[path] = FileType.Other

    def to_abs_path(self, path):
        if path.startswith(os.sep):
            xpath = path.strip()
        else:
            xpath = self.code_dir + os.sep + path.strip()
        return os.path.abspath(xpath)

    def dump(self):
        sorted_list = sorted(self.out_dict.items(), key=lambda x: x[1])
        for item in sorted_list:
            print(item)


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    _blt = os.path.realpath("/home/wu/work/nxp/wr_atf/arm-trusted-firmware/build/fawcgw/release")
    _code = os.path.realpath("/home/wu/work/nxp/wr_atf/arm-trusted-firmware")
    _file = "./test_example/atf/crc8.d"
    obj = atf_d_Parser(_blt, _code, _file)
    obj.parse()
    obj.dump()
