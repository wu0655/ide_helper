#!/usr/bin/python3
import os
import shutil
import sys

from common.vscode_config.CppPluginJsonHandler import CppPluginJsonHandler
from common.vscode_config.SettingsJsonHandler import SettingsJsonHandler
from common.vscode_config.TasksJsonHandler import TasksJsonHandler


class VscodeWorkspaceGenerator(object):

    def __init__(self, blt_dir, code_dir, path):
        self.shell_dir = path
        self.blt_dir = os.path.realpath(blt_dir)
        self.code_dir = os.path.realpath(code_dir)

    def init(self):
        self.create_vscode_workspace()
        handler = SettingsJsonHandler(self.blt_dir, self.code_dir, self.shell_dir)
        handler.do_handle()
        handler = CppPluginJsonHandler(self.blt_dir, self.code_dir, self.shell_dir)
        handler.do_handle()
        handler = TasksJsonHandler(self.blt_dir, self.code_dir, self.shell_dir)
        handler.do_handle()

    def output(self):
        pass

    def create_vscode_workspace(self):
        path = os.path.join(self.code_dir, '.vscode')
        if not os.path.exists(path):
            os.mkdir(path)
        elif os.path.isdir(path):
            pass
        else:
            os.remove(path)
            os.mkdir(path)

        fn_list = ['settings.json', 'c_cpp_properties.json', 'tasks.json']
        for fn in fn_list:
            if not os.path.exists(os.path.join(path, fn)):
                shutil.copy(os.path.join(self.shell_dir, './vscode_template', fn), os.path.join(path, fn))


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 2:
        exit(0)

    if len(sys.argv) > 3:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(sys.argv[2])
        shell_dir = sys.argv[3]
    else:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(_blt_dir + os.sep + "source")
        shell_dir = sys.argv[2]

    obj = VscodeWorkspaceGenerator(_blt_dir, _src_dir, shell_dir)
    obj.init()
    obj.output()

