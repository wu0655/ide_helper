#!/usr/bin/env bash

__script_dir=$(
  cd $(dirname ${BASH_SOURCE[0]})
  pwd
)
pushd ${__script_dir}
rm -fv *.txt && rm -fv ln_set.sh && rm -fv mkdir_set.sh && rm -fv rm_set.sh && rm -fv *.json
popd
