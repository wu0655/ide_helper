# example ./do_all.sh ~/work/nxp/wr_atf/u-boot/out/ ~/work/vs_temp/

if [ $# -lt 2 ] ; then
	echo "USAGE: $0 from to"
	echo " e.g.: $0 out_dir ws_dir"
	exit 1;
fi

__proj_dir=$2/uboot
__file_list=uboot_filelist.txt

source cleanup.sh
PYTHONPATH=${PWD}/.. python3 UbootOutDirAnalyzer.py $1 ${__file_list}
PYTHONPATH=${PWD}/.. python3 ../common/ShellScriptGenerator.py $1 ${__proj_dir} ${__file_list}

# generate vscode workspace
PYTHONPATH=${PWD}/.. python3 ../common/generate_compdb.py  -O $1
PYTHONPATH=${PWD}/.. python3 ../common/VscodeConfigGenerator.py $1 ${__file_list}
cp -fv compile_commands.json $1/source/
mkdir -p  $1/source/.vscode
cp -fv vscode_template/* $1/source/.vscode/
cp -fv ../common/generate_compdb.py $1/source/.vscode/
cp -fv settings.json $1/source/.vscode/settings.json
