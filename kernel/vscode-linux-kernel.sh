pushd $1/source
#git clone git@github.com:amezin/vscode-linux-kernel.git .vscode
cp -rf ~/work/github/vscode-linux-kernel ./vscode
python .vscode/generate_compdb.py -O $1
popd

