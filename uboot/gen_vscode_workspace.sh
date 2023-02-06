#!/usr/bin/env bash

__usage="USAGE: $0 built_out_dir"
if [ $# -lt 1 ]; then
  echo ${__usage}
  exit 1
fi

__script_dir=$(
  cd $(dirname ${BASH_SOURCE[0]}) || exit
  pwd
)

source ${__script_dir}/cleanup.sh

PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/UbootOutDirAnalyzer.py $1 ${__script_dir}

#
# generate vscode workspace
#

# generate compile_commands.json
PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/../common/generate_compdb.py -O $1
# generate settings.json
PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/../common/VscodeWorkspaceGenerator.py $1 ${__script_dir}
