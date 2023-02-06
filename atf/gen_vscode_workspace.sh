#!/usr/bin/env bash

__usage="USAGE: $0 built_out_dir code_dir (option)make_log"
if [ $# -lt 2 ]; then
  echo ${__usage}
  exit 1
fi

__script_dir=$(
  cd $(dirname ${BASH_SOURCE[0]}) || exit
  pwd
)

source ${__script_dir}/cleanup.sh

PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/AtfOutDirAnalyzer.py $1 $2 ${__script_dir}

#
# generate vscode workspace
#
PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/../common/VscodeWorkspaceGenerator.py $1 $2 ${__script_dir}
PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/AtfVscodeCppPluginJsonHandler.py $1 $2 ${__script_dir} $3

