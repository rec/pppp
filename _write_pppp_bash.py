from pathlib import Path
import datetime
import sys

if __name__ == '__main__':
    tmpl = open('pppp.sh.tmpl').read()
    with open('pppp.sh', 'w') as fp:
        contents = tmpl.format(
            now=datetime.datetime.utcnow(),
            program=Path(sys.argv[0]).name,
            code=open('pppp.py').read(),
        )
        fp.write(contents)
        print('Wrote pppp.sh')
