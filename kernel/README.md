# guide

## download tool
```
cd kernel_code_path
git clone https://github.com/wu0655/ide_helper.git  .ide_helper
```

## generate filelist
```
./.ide_helper/kernel/gen_filelist.sh kernel_build_out
```
- ./.ide_helper/kernel/filelist.txt is the output

## generate vscode workspace
```
./.ide_helper/kernel/gen_vscode_workspace.sh kernel_build_out
```
- ./.vscode  is the vscode workspace setting