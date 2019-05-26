FILE="""\
pppp() {{
    DIR=`python - $@ <<'___EOF'
{0}
___EOF`
    if [ $DIR ] ; then
        echo "--> $DIR"
        cd $DIR
    fi
}}
"""

if __name__ == '__main__':
    with open('pppp.sh', 'w') as fp:
       fp.write(FILE.format(open('pppp.py').read()))
