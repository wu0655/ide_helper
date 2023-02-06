#!/usr/bin/env bash

__usage="USAGE: $0 built_out_dir code_dir"
if [ $# -lt 2 ]; then
  echo ${__usage}
  exit 1
fi

__script_dir=$(
  cd $(dirname ${BASH_SOURCE[0]})
  pwd
)

source ${__script_dir}/cleanup.sh

PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/AtfOutDirAnalyzer.py $1 $2 ${__script_dir}
