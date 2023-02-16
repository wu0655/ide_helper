# guide

## download tool
```
cd u-boot_code_path
git clone https://github.com/wu0655/ide_helper.git  .ide_helper
```

## generate filelist
```
./.ide_helper/uboot/gen_filelist.sh uboot_build_out
```
- ./.ide_helper/uboot/filelist.txt is the output

## generate vscode workspace
```
./.ide_helper/uboot/gen_vscode_workspace.sh uboot_build_out
```
- ./.vscode  is the vscode workspace setting