#!/usr/bin/python3
import os
import sys


class ShellScriptGenerator(object):
    # path
    file_path = ""
    ws_dir = ""
    code_dir = ""
    blt_dir = ""

    code_set = set()
    ln_set = set()
    mkdir_set = set()
    rm_set = set()

    def __init__(self, blt_dir, code_dir, workspace_dir, path):
        self.file_path = path
        self.ws_dir = workspace_dir
        self.blt_dir = os.path.realpath(blt_dir)
        self.code_dir = os.path.realpath(code_dir)

    def init(self):
        # parse source
        with open(self.file_path, 'r') as f:
            for line in f.readlines():
                path = os.path.abspath(line).strip()
                if path.startswith(self.blt_dir):
                    self.handle_one_gen_file(path)
                else:
                    self.handle_one_src_file(path)
                    self.code_set.add(path)
        # self.gen_rm_for_not_built_file()

    def gen_rm_for_not_built_file(self):
        for root, dirs, files in os.walk(self.code_dir + "/arch"):
            for f in files:
                self.handle_one_for_rm(root, f)
        for root, dirs, files in os.walk(self.code_dir + "/board"):
            for f in files:
                self.handle_one_for_rm(root, f)
        for root, dirs, files in os.walk(self.code_dir + "/drivers"):
            for f in files:
                self.handle_one_for_rm(root, f)

    def handle_one_for_rm(self, root, f):
        t = os.path.basename(f)
        if t.endswith(".S") or t.endswith(".h") or t.endswith(".c") or t.endswith(".dtsi") or t.endswith(".dts"):
            filepath = os.path.join(os.path.abspath(root), f)
            if filepath not in self.code_set:
                cmd = "rm -f " + filepath
                self.rm_set.add(cmd)

    def handle_one_src_file(self, src):
        dst = os.path.abspath(self.ws_dir + os.sep + src[len(self.code_dir):len(src)])
        dst_dir = os.path.dirname(dst)
        self.mkdir_set.add("mkdir -p " + dst_dir)
        cmd = "ln -s " + src.strip() + " " + dst.strip()
        self.ln_set.add(cmd)

    def handle_one_gen_file(self, src):
        dst = self.ws_dir + os.sep + "out" + os.sep + src[len(self.blt_dir):len(src)]
        dst_dir = os.path.dirname(os.path.abspath(dst))
        self.mkdir_set.add("mkdir -p " + dst_dir)
        cmd = "ln -s " + src.strip() + " " + dst.strip()
        self.ln_set.add(cmd)

    def dump(self):
        print("-------code_set----------")
        for x in self.code_set:
            print(x)

    @staticmethod
    def flush_to_file(in_set, name):
        fn = open(name, 'w')
        for x in in_set:
            fn.write(x + '\n')
        fn.close()

    def output(self):
        self.flush_to_file(sorted(self.mkdir_set), "mkdir_set.sh")
        self.flush_to_file(sorted(self.ln_set), "ln_set.sh")
        self.flush_to_file(sorted(self.rm_set), "rm_set.sh")


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) > 4:
        # atf
        obj = ShellScriptGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        # kernel/uboot
        obj = ShellScriptGenerator(sys.argv[1], os.path.realpath(sys.argv[1] + os.sep + "source"), sys.argv[2], sys.argv[3])
    # obj.handle_one_src_file("/data/work/nxp/wr_atf/u-boot/arch/arm/cpu/armv8/s32/s32-gen1/sgmii/sgmii.c")
    obj.init()
    obj.output()
