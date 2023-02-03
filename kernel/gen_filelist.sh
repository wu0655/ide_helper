#!/usr/bin/env bash

__usage="USAGE: $0 built_out_dir"
__script_dir=$(
  cd $(dirname ${BASH_SOURCE[0]})
  pwd
)

if [ $# -lt 1 ]; then
  echo ${__usage}
  exit 1
fi

source ${__script_dir}/cleanup.sh

PYTHONPATH=${__script_dir}/.. python3 ${__script_dir}/KernelOutDirAnalyzer.py $1 ${__script_dir}
