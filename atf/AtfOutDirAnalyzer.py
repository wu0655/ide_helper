#!/usr/bin/python3
import os
import sys
import time

from common.FileType import FileType
from common.file_parser.atf_d_Parser import atf_d_Parser
from common.file_parser.atf_o_d_Parser import atf_o_d_Parser


class AtfOutDirAnalyzer(object):
    out_name = "filelist.txt"
    out_set = set()
    other_set = set()
    wildcard_set = set()

    blt_dir = ""
    code_dir = ""

    def __init__(self, blt, code, name):
        if len(name) > 0:
            self.out_name = name
        self.blt_dir = blt
        self.code_dir = code

    def init(self):
        code_files_db = []
        for root, dirs, files in os.walk(self.blt_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".o.d"):
                    parser = atf_o_d_Parser(self.blt_dir, self.code_dir, filepath)
                    parser.parse()
                    code_files_db.append(parser.out())

                elif filepath.endswith(".d"):
                    parser = atf_d_Parser(self.blt_dir, self.code_dir, filepath)
                    parser.parse()
                    code_files_db.append(parser.out())

        self.merge_set(code_files_db)
        self.scan_auto_gen_h()

    def merge_set(self, db):
        for index in range(len(db)):
            for key in db[index]:
                if db[index][key] == FileType.Other:
                    self.other_set.add(key)
                elif db[index][key] == FileType.Wildcard:
                    self.wildcard_set.add(key)
                elif db[index][key] == FileType.Code:
                    self.out_set.add(key)

    def scan_auto_gen_h(self):
        for root, dirs, files in os.walk(self.blt_dir + os.sep):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".h") and filepath.endswith(".c") and os.path.getsize(filepath) > 0:
                    self.out_set.add(filepath)

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
        fn = open(name, 'w')
        for x in in_set:
            fn.write(x + '\n')
        fn.close()

    def output(self):
        self.flush_to_file(sorted(self.out_set), self.out_name)
        self.flush_to_file(sorted(self.other_set), "other_set.txt")
        self.flush_to_file(sorted(self.wildcard_set), "wildcard_set.txt")


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    # print('len=', len(sys.argv))

    if not os.path.exists(sys.argv[1]):
        print("input parameter error")
        sys.exit()
    else:
        test_blt_path = os.path.realpath(sys.argv[1])

    if not os.path.exists(sys.argv[1]):
        print("input parameter error")
        sys.exit()
    else:
        test_blt_path = os.path.realpath(sys.argv[1])

    if not os.path.exists(sys.argv[2]):
        print("input parameter error")
        sys.exit()
    else:
        test_code_path = os.path.realpath(sys.argv[2])

    if len(sys.argv) > 3:
        test_name = sys.argv[3]
    else:
        test_name = ""

    begin = time.time()
    obj = AtfOutDirAnalyzer(test_blt_path, test_code_path, test_name)
    obj.init()
    obj.output()
    end = time.time()
    print("takes %.2f second" % (end - begin))