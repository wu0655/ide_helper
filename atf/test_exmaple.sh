#!/usr/bin/env bash

__script_dir=$(cd $(dirname ${BASH_SOURCE[0]}); pwd)
${__script_dir}/gen_filelist.sh \
    ~/work/nxp/wr_atf/arm-trusted-firmware/build/batman/release/ \
    ~/work/nxp/wr_atf/arm-trusted-firmware

${__script_dir}/gen_vscode_workspace.sh \
    ~/work/nxp/wr_atf/arm-trusted-firmware/build/batman/release/ \
    ~/work/nxp/wr_atf/arm-trusted-firmware \
    ~/work/nxp/wr_atf/arm-trusted-firmware/make_help.log

