#!/usr/bin/python3
import os
import sys

from common.ShellScriptGenerator import ShellScriptGenerator


class AtfShellScriptGenerator(ShellScriptGenerator):
    code_dir_set = set()

    def init(self):
        super(AtfShellScriptGenerator, self).init()
        # add Makefile under root dir
        self.handle_makefile()

    def handle_one_src_file(self, src):
        super(AtfShellScriptGenerator, self).handle_one_src_file(src)
        d = os.path.dirname(src)
        tmp = d[len(self.code_dir):len(d)].strip().split("/")
        s = ""
        for index in range(len(tmp)):
            if len(tmp[index]) > 0:
                s = s + os.sep + tmp[index]
                self.code_dir_set.add(os.path.realpath(self.code_dir + s))

    def handle_makefile(self):
        mk_set = set()
        self.code_dir_set.add(self.code_dir)
        for d in self.code_dir_set:
            # add Makefile
            self.find_mk_file(mk_set, d)

        for src_makefile in mk_set:
            dst_makefile = os.path.abspath(self.ws_dir + os.sep + src_makefile[len(self.code_dir):len(src_makefile)])
            cmd = "ln -s " + src_makefile.strip() + " " + dst_makefile.strip()
            self.ln_set.add(cmd)

        cmd = "ln -s " + self.code_dir + os.sep + "make_helpers " + self.ws_dir + os.sep + "make_helpers"
        self.ln_set.add(cmd)

    @staticmethod
    def find_mk_file(mk_set, dir_name):
        for file in os.listdir(dir_name):
            if file.endswith(".mk") or file.endswith("akefile"):
                # print("makefile=", file)
                mk_set.add(os.path.realpath(dir_name + os.sep + file))

    def dump(self):
        super(AtfShellScriptGenerator, self).dump()
        print("-------code_dir_set----------")
        for x in self.code_dir_set:
            print(x)


if __name__ == "__main__":
    print('input=' + str(sys.argv))

    if len(sys.argv) > 4:
        # atf
        obj = AtfShellScriptGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        # obj.handle_one_src_file("/data/work/nxp/wr_atf/u-boot/arch/arm/cpu/armv8/s32/s32-gen1/sgmii/sgmii.c")
        obj.init()
        obj.output()
        # obj.dump()
