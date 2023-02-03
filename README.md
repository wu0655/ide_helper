# 1. bsp_ide_help
- depend on python3 and code build ok
- parse out directory to generate file list which are built.
  - use the file list directly, such vim/source insight
  - create workspace for vscode
  - support kernel, u-boot, arm-trusted-firmware
- tested on ubuntu18.04 with python3.9, bash

## 1.1. kernel
- cd kernel
- run do_all.sh, task test_do_all as example on commandline
### 1.1.1. vim/source insight
- use kernel_filelist.txt
### 1.1.2. vscode
- workspace is created under kernel_code_path
- edit .vscode/c_cpp_properties.json
  - edit env
- edit .vscode/*.json as needed

## 1.2. u-boot
- cd uboot
- run do_all.sh, task test_do_all as example on commandline
### 1.2.1. vim/source insight
- use uboot_filelist.txt
### 1.2.2. vscode
- workspace is created under uboot_code_path
- edit .vscode/c_cpp_properties.json
  - edit env
- edit .vscode/*.json as needed

## 1.3. arm-trusted-firmware
- cd atf
- run do_all.sh, task test_do_all as example on commandline
### 1.3.1. vim/source insight
- use atf_filelist.txt
### 1.3.2. vscode
#### 1.3.2.1. workspace
- workspace is created under atf_code_path
- edit .vscode/c_cpp_properties.json
  - edit env
- edit .vscode/*.json as needed
#### 1.3.2.2. add defines in c_cpp_properties.json automatically
- generate make_help.log
  - use make with '-p'
  - example
```bash
export CROSS_COMPILE=gcc_path
make -p ARCH=aarch64 PLAT=s32g2 BL33= u-boot-s32.bin 2>&1 | tee make_help.log
```
- re-run do_all.sh
    