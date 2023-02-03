# example ./do_all.sh ~/work/nxp/wr_atf/u-boot/out/ ~/work/vs_temp/

if [ $# -lt 3 ]; then
  echo "USAGE: $0 from to"
  echo " e.g.: $0 blt_dir code_dir ws_dir"
  exit 1
fi

__proj_dir=$3/atf
__file_list=atf_filelist.txt
__code_dir=$2

source cleanup.sh

PYTHONPATH=${PWD}/.. python3 AtfOutDirAnalyzer.py $1 $2 ${__file_list}
PYTHONPATH=${PWD}/.. python3 AtfShellScriptGenerator.py $1 $2 ${__proj_dir} ${__file_list}

# generate vscode workspace
PYTHONPATH=${PWD}/.. python3 ../common/VscodeConfigGenerator.py $1 $2 ${__file_list}
mkdir -p ${__code_dir}/.vscode
cp -fv vscode_template/* ${__code_dir}/.vscode/
cp -fv settings.json ${__code_dir}/.vscode/

if [ -f "$4" ]; then
	PYTHONPATH=${PWD}/.. python3 AtfVscodeCppPluginConfigGenerator.py $4
	cp -fv c_cpp_properties.json ${__code_dir}/.vscode/
fi
