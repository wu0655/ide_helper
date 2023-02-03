#!/usr/bin/python3
import os
import sys

from common.FileType import FileType, ParseResultFile


class OutDirAnalyzer(object):
    shell_dir = '.'
    out_set = set()
    other_set = set()
    wildcard_set = set()

    blt_dir = ""
    code_dir = ""

    def __init__(self, path, name):
        if len(name) > 0:
            self.shell_dir = name
        self.blt_dir = os.path.realpath(path)
        self.code_dir = os.path.realpath(path + os.sep + "source")

    def init(self):
        pass

    def scan_auto_gen_h(self):
        for root, dirs, files in os.walk(self.blt_dir + os.sep + "include"):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".h") and os.path.getsize(filepath) > 0:
                    self.out_set.add(filepath)

    def merge_set(self, db):
        for index in range(len(db)):
            for key in db[index]:
                if db[index][key] == FileType.Other:
                    self.other_set.add(key)
                elif db[index][key] == FileType.Wildcard:
                    self.wildcard_set.add(key)
                elif db[index][key] == FileType.Code:
                    self.out_set.add(key)

    def dump(self):
        print("-------c_set----------")
        for x in self.out_set:
            print(x)
        print("-------other_set----------")
        for x in self.other_set:
            print(x)
        print("-------wildcard_set----------")
        for x in self.wildcard_set:
            print(x)

    @staticmethod
    def flush_to_file(in_set, name):
        if len(in_set) > 0:
            fn = open(name, 'w')
            for x in in_set:
                fn.write(x + '\n')
            fn.close()
            print("output file ", name)

    def output(self):
        self.flush_to_file(sorted(self.out_set), os.path.join(self.shell_dir, ParseResultFile.Code))
        self.flush_to_file(sorted(self.other_set), os.path.join(self.shell_dir, ParseResultFile.Other))
        self.flush_to_file(sorted(self.wildcard_set), os.path.join(self.shell_dir, ParseResultFile.Wildcard))

