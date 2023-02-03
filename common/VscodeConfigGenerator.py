#!/usr/bin/python3
import json
import os
import sys
from collections import OrderedDict


class VscodeConfigGenerator(object):
    code_file_set = set()
    code_dir_set = set()
    dir_exclude_dict = {}
    file_exclude_dict = {}

    def __init__(self, blt_dir, code_dir, path):
        self.file_path = path
        self.blt_dir = os.path.realpath(blt_dir)
        self.code_dir = os.path.realpath(code_dir)

    def init(self):
        with open(self.file_path, 'r') as f:
            for line in f.readlines():
                path = os.path.abspath(line).strip()
                if path.startswith(self.blt_dir):
                    pass
                elif path.startswith(self.code_dir):
                    self.handle_one_src_file(path)
                    self.code_file_set.add(path)

        self.scan_dir(self.code_dir)
        self.exclude_file()

    def exclude_file(self):
        for d in self.code_dir_set:
            # print('d=', d)
            for fn in os.listdir(d):
                path = os.path.join(d, fn)
                if os.path.isfile(path) and path not in self.code_file_set:
                    strip_head_len = len(self.code_dir) + 1
                    key = path[strip_head_len:len(path)].strip()
                    self.dir_exclude_dict[key] = True

    def handle_one_src_file(self, src):
        d = os.path.dirname(src)
        tmp = d[len(self.code_dir):len(d)].strip().split("/")
        s = ""
        for index in range(len(tmp)):
            if len(tmp[index]) > 0:
                s = s + os.sep + tmp[index]
                self.code_dir_set.add(os.path.realpath(self.code_dir + s))

    def scan_dir(self, root_dir):
        for lists in os.listdir(root_dir):
            path = os.path.join(root_dir, lists)
            if os.path.isdir(path):
                if path not in self.code_dir_set:
                    strip_head_len = len(self.code_dir) + 1
                    key = path[strip_head_len:len(path)].strip()
                    self.dir_exclude_dict[key] = True
                else:
                    self.scan_dir(path)

    def output(self):
        path = "./vscode_template/settings.json"
        if os.path.exists(path):
            with open(path, "r") as jsonFile:
                settings = json.load(jsonFile)
                settings["files.exclude"] = OrderedDict(sorted(self.dir_exclude_dict.items()))
        else:
            settings = {"files.exclude": OrderedDict(sorted(self.dir_exclude_dict.items()))}
        with open("settings.json", 'w') as f:
            json.dump(settings, f, indent=4)

    def dump(self):
        print("-------code_dir_set----------")
        for x in self.code_dir_set:
            print(x)


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 2:
        exit(0)

    if len(sys.argv) > 3:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(sys.argv[2])
        filelist = sys.argv[3]
    else:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(_blt_dir + os.sep + "source")
        filelist = sys.argv[2]

    obj = VscodeConfigGenerator(_blt_dir, _src_dir, filelist)
    # obj.handle_one_src_file("/data/work/nxp/wr_atf/u-boot/arch/arm/cpu/armv8/s32/s32-gen1/sgmii/sgmii.c")
    obj.init()
    obj.output()
    # obj.dump()

"""
    _blt_dir = os.path.realpath("F:\\nxp\\wr_atf\\kernel\\out")
    _src_dir = os.path.realpath(_blt_dir + os.sep + "source")
    filelist = "F:\\github\\tools_in_python\\export_built_files\\kernel\\kernel_filelist.txt"
"""


