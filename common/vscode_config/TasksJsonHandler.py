#!/usr/bin/python3
import os
import sys

from common.FileType import VsCodeJsonConfig
from common.vscode_config.JsonHandler import JsonHandler


class TasksJsonHandler(JsonHandler):
    target_json_file = VsCodeJsonConfig.Task

    def do_update(self):
        for idx, ta in enumerate(self.json_content['tasks']):
            cmd = ta['command']
            if cmd.strip().endswith('gen_vscode_workspace.sh'):
                self.json_content['tasks'][idx]['args'][0] = self.blt_dir
        return True


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) <= 3:
        exit(1)

    if len(sys.argv) > 3:
        _blt_dir = os.path.realpath(sys.argv[1])
        _src_dir = os.path.realpath(sys.argv[2])
        shell_dir = sys.argv[3]

        obj = TasksJsonHandler(_blt_dir, _src_dir, shell_dir)
        obj.do_handle()
