import json
import os


class JsonHandler(object):
    target_json_file = ""
    json_content = {}

    def __init__(self, blt_dir, code_dir, path):
        self.blt_dir = os.path.realpath(blt_dir)
        self.code_dir = os.path.realpath(code_dir)
        self.shell_dir = path

    def do_update(self):
        return False

    def do_handle(self):
        path = os.path.join(self.code_dir, '.vscode', self.target_json_file)
        if not os.path.isfile(path):
            path = os.path.join('./vscode_template', self.target_json_file)

        if os.path.exists(path):
            with open(path, "r") as jsonFile:
                self.json_content = json.load(jsonFile)

            if self.do_update():
                with open(path, 'w') as f:
                    json.dump(self.json_content, f, indent=4)
