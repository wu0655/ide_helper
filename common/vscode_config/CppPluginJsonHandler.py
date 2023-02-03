#!/usr/bin/python3
import json
import os
import sys

from common.FileType import VsCodeJsonConfig, ParseResultFile
from common.vscode_config.JsonHandler import JsonHandler


class CppPluginJsonHandler(JsonHandler):
    target_json_file = VsCodeJsonConfig.CppPlugin

    def do_update(self):
        path = os.path.join(self.shell_dir, ParseResultFile.GccPath)
        if not os.path.isfile(path):
            return False
        with open(path, "r") as gcc_file:
            gcc_path = gcc_file.readline().strip()
            self.json_content['env']['myCompilerPath'] = gcc_path
            return True


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 3:
        exit(1)

    if len(sys.argv) > 3:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(sys.argv[2])
        shell_dir = sys.argv[3]

        obj = CppPluginJsonHandler(_blt_dir, _src_dir, shell_dir)
        obj.do_handle()
