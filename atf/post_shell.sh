#./test_do_all.sh 
./ln2cp.sh ln_set.sh 
rm -rf ~/work/vs_work/atf
source mkdir_set.sh 
source ln_set.sh 
pushd ~/work/vs_work/atf/
git init .
git add *
git commit -m "create git from build"
popd
