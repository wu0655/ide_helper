# ./do_all.sh ~/work/nxp/wr_atf/kernel/out

if [ $# -lt 1 ] ; then
	echo "USAGE: $0 from to"
	echo " e.g.: $0 out_dir"
	exit 1;
fi

#__proj_dir=$2/kernel
__file_list=kernel_filelist.txt

source cleanup.sh

PYTHONPATH=${PWD}/.. python3 KernelOutDirAnalyzer.py $1 ${__file_list}

#
# generate vscode workspace
#

# generate compile_commands.json
PYTHONPATH=${PWD}/.. python3 ../common/generate_compdb.py  -O $1
# generate settings.json
PYTHONPATH=${PWD}/.. python3 ../common/VscodeConfigGenerator.py $1 ${__file_list}
