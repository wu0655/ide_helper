#!/usr/bin/python3
import math
import multiprocessing
import os
import sys
import time

from common.OutDirAnalyzer import OutDirAnalyzer
from common.file_parser.d_pre_tmp_Parser import d_pre_tmp_Parser
from common.file_parser.o_cmd_Parser import o_cmd_Parser


def print_progress_bar(progress):
    progress_bar = '[' + '|' * int(50 * progress) + '-' * int(50 * (1.0 - progress)) + ']'
    print('\r', progress_bar, "{0:.1%}".format(progress), end='\r', file=sys.stderr)


class KernelOutDirAnalyzer(OutDirAnalyzer):
    def init(self):
        # walk dir to find tmp files
        cmd_files = []
        for root, dirs, files in os.walk(self.blt_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".o.cmd"):
                    cmd_files.append(filepath)
        dt_tmp_files = []
        for root, dirs, files in os.walk(self.blt_dir + os.sep + "arch"):
            for f in files:
                filepath = os.path.join(root, f)
                if filepath.endswith(".d.pre.tmp"):
                    dt_tmp_files.append(filepath)

        # parse tmp files
        n_processed = 0
        code_files_db = []
        if multiprocessing.cpu_count() > 16:
            pool_max = 16
        else:
            pool_max = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(pool_max)
        total = len(cmd_files) + len(dt_tmp_files)
        try:
            for compdb_chunk in pool.imap_unordered(self.o_cmd_parser, cmd_files,
                                                    chunksize=int(math.sqrt(len(cmd_files)))):
                code_files_db.append(compdb_chunk)
                n_processed += 1
                print_progress_bar(n_processed / total)

            for compdb_chunk in pool.imap_unordered(self.dt_cmd_parser, dt_tmp_files,
                                                    chunksize=int(math.sqrt(len(dt_tmp_files)))):
                code_files_db.append(compdb_chunk)
                n_processed += 1
                print_progress_bar(n_processed / total)
        finally:
            pool.terminate()
            pool.join()
        print("")

        # output
        self.merge_set(code_files_db)
        self.scan_auto_gen_h()

    def o_cmd_parser(self, filepath):
        parser = o_cmd_Parser(self.blt_dir, self.code_dir, filepath)
        parser.parse()
        return parser.out()

    def dt_cmd_parser(self, filepath):
        parser = d_pre_tmp_Parser(self.blt_dir, self.code_dir, filepath)
        parser.parse()
        return parser.out()

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
        test_path = os.path.realpath(sys.argv[1])

    if len(sys.argv) > 2:
        name = sys.argv[2]
    else:
        name = ""

    begin = time.time()
    obj = KernelOutDirAnalyzer(test_path, name)
    obj.init()
    obj.output()
    end = time.time()
    print("takes %.2f second" % (end - begin))
