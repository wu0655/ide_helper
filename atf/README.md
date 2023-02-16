# guide

## download tool
```
cd u-boot_code_path
git clone https://github.com/wu0655/ide_helper.git  .ide_helper
```

## generate filelist
```
./.ide_helper/atf/gen_filelist.sh atf_build_out
```
- ./.ide_helper/atf/filelist.txt is the output

## generate vscode workspace
```
./.ide_helper/atf/gen_vscode_workspace.sh atf_build_out
```
- ./.vscode  is the vscode workspace setting
    