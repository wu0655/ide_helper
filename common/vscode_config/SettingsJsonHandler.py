#!/usr/bin/python3
import os
import sys
from collections import OrderedDict

from common.FileType import ParseResultFile, VsCodeJsonConfig
from common.vscode_config.JsonHandler import JsonHandler


class SettingsJsonHandler(JsonHandler):
    flag_add_makefile_to_workspace = True

    target_json_file = VsCodeJsonConfig.Setting

    code_file_set = set()
    code_dir_set = set()
    dir_exclude_dict = {}
    file_exclude_dict = {}

    def init(self):
        filelist = os.path.join(self.shell_dir, ParseResultFile.Code)
        with open(filelist, 'r') as f:
            for line in f.readlines():
                path = os.path.abspath(line).strip()
                if path.startswith(self.blt_dir):
                    pass
                elif path.startswith(self.code_dir):
                    self.handle_one_src_file(path)
                    self.code_file_set.add(path)
        self.scan_dir(self.code_dir)
        self.add_makefile_to_workspace() # must called before self.exclude_file
        self.exclude_file()

    @staticmethod
    def is_mk_file(path):
        if path.endswith(".mk") or os.path.basename(path) == "Makefile" or os.path.basename(path) == "Kconfig":
            return True
        else:
            return False

    def add_makefile_to_workspace(self):
        if not self.flag_add_makefile_to_workspace:
            return
        for path in self.code_dir_set:
            for name in os.listdir(path):
                fn = os.path.join(path, name)
                if self.is_mk_file(fn):
                    self.code_file_set.add(fn)

    def exclude_file(self):
        for d in self.code_dir_set:
            # print('d=', d)
            for fn in os.listdir(d):
                path = os.path.join(d, fn)
                if os.path.isfile(path) and path not in self.code_file_set:
                    strip_head_len = len(self.code_dir) + 1
                    key = path[strip_head_len:len(path)].strip()
                    self.file_exclude_dict[key] = True

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

    def do_update(self):
        self.init()
        exclude_dict = {**self.file_exclude_dict, **self.dir_exclude_dict}
        if len(exclude_dict) == 0:
            print("no valid exclude found")
            return False

        self.json_content["files.exclude"] = OrderedDict(sorted(exclude_dict.items()))
        return True


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 3:
        exit(1)

    if len(sys.argv) > 3:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(sys.argv[2])
        shell_dir = sys.argv[3]

        obj = SettingsJsonHandler(_blt_dir, _src_dir, shell_dir)
        obj.do_handle()
