from enum import Enum


class FileType(Enum):
    Code = 1
    Other = 2
    Wildcard = 3


class ParseResultFile(object):
    Code = "filelist.txt"
    Other = "other_set.txt"
    Wildcard = "wildcard_set.txt"
    GccPath = "gcc_path.txt"


class VsCodeJsonConfig(object):
    Setting = "settings.json"
    Task = "tasks.json"
    CppPlugin = "c_cpp_properties.json"
    BrowseDb = "browse.vc.db"

