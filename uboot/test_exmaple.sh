#!/usr/bin/env bash

__script_dir=$(cd $(dirname ${BASH_SOURCE[0]}); pwd)
${__script_dir}/gen_vscode_workspace.sh ~/work/nxp/wr_atf/u-boot/out

