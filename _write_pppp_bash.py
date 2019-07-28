from pathlib import Path
import datetime
import subprocess
import sys


def main():
    tmpl = open('pppp.sh.tmpl').read()
    code = open('pppp.py').read()

    contents = tmpl.format(
        code=_replace_git_info(code),
        now=datetime.datetime.utcnow(),
        program=Path(sys.argv[0]).name,
    )
    with open('pppp.sh', 'w') as fp:
        fp.write(contents)
    print('Wrote pppp.sh')


def _replace_git_info(code):
    commit_id = _git('rev-parse HEAD')[0]
    branch = _git('symbolic-ref --short HEAD')[0]
    upstream = _git('rev-parse --abbrev-ref --symbolic-full-name @{u}')[0]
    remote, upstream_branch = upstream.split('/')

    for r in _git('remote -v'):
        name, upstream, *_ = r.split()
        if name == remote:
            break
    else:
        raise ValueError('No such remote!')

    for name in 'commit_id', 'branch', 'upstream', 'upstream_branch':
        code = code.replace('{%s}' % name, locals()[name])
    return code


def _git(cmd):
    cmd = ['git'] + cmd.split()
    return subprocess.check_output(cmd, encoding='utf-8').splitlines()


if __name__ == '__main__':
    main()
