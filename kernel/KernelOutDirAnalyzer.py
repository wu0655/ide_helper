#!/usr/bin/python3
import math
import multiprocessing
import os
import sys
import time

from common.FileType import ParseResultFile
from common.OutDirAnalyzer import OutDirAnalyzer
from common.file_parser.d_pre_tmp_Parser import d_pre_tmp_Parser
from common.file_parser.o_cmd_Parser import o_cmd_Parser


def print_progress_bar(progress):
    progress_bar = '[' + '|' * int(50 * progress) + '-' * int(50 * (1.0 - progress)) + ']'
    print('\r', progress_bar, "{0:.1%}".format(progress), end='\r', file=sys.stderr)


class KernelOutDirAnalyzer(OutDirAnalyzer):
    gcc_path = ""

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

        # try to get gcc, it should be very fast
        self.parse_gcc(cmd_files)

    def o_cmd_parser(self, filepath):
        parser = o_cmd_Parser(self.blt_dir, self.code_dir, filepath)
        parser.parse()
        return parser.out()

    def dt_cmd_parser(self, filepath):
        parser = d_pre_tmp_Parser(self.blt_dir, self.code_dir, filepath)
        parser.parse()
        return parser.out()

    def parse_gcc(self, files):
        for fn in files:
            # fn = "/data/work/nxp/wr_atf/tda4_kernel/out/block/.blk-pm.o.cmd"
            with open(fn, 'r') as f:
                line = f.readline().strip()
                tmp = line.split(":=")
                if len(tmp) >= 2:
                    path = tmp[1].strip().split(" ")[0].strip()
                    if path.endswith("gcc"):
                        self.gcc_path = path
                        print("gcc is found at ", path)
                        break

    def output(self):
        super(KernelOutDirAnalyzer, self).output()
        if len(self.gcc_path) > 0:
            gcc_file = os.path.join(self.shell_dir, ParseResultFile.GccPath)
            fn = open(gcc_file, 'w')
            fn.write(self.gcc_path)
            fn.close()
            print("output file ", gcc_file)


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 2:
        exit(0)

    _blt_dir = os.path.realpath(sys.argv[1])
    _src_dir = os.path.realpath(_blt_dir + os.sep + "source")
    shell_dir = sys.argv[2]

    begin = time.time()
    obj = KernelOutDirAnalyzer(_blt_dir, shell_dir)
    obj.init()
    obj.output()
    end = time.time()
    print("takes %.2f second" % (end - begin))
