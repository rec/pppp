# set -Eexo pipefail

DIR=`python - <<'___EOF'
print('/code')
___EOF`

if [ $DIR ] ; then
    echo $DIR
    cd $DIR
else
    echo '(no project)
fi
