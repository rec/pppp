"""
pppp: Project Push Pop Project

Keep a persistent stack of working project directories
"""

import inspect
import json
import os
import sys

PPPP_QUIET_ENV = 'PPPP_QUIET'
QUIET = os.environ.get(PPPP_QUIET_ENV, '')
CONFIG_DIR = os.environ.get('XDG_CONFIG_HOME', '$HOME/.config')

COMMANDS = (
    'cd', 'clear', 'info', 'list', 'pop', 'push', 'rotate', 'swap', 'undo',
)

VERSION = '0.9.2'
ICON = u'\U0001f37f'
DESCRIPTION = """\
{icon} pppp: a stack of project directories as a tiny bash utility {icon}
v{version}

'pppp' is a persistent stack of project directories.
Very useful for people who get interrupted a lot.

The 'pppp' commands are {first}, and {rest}.

You only need to type the first letter of any command.

'pppp' with no arguments changes directory to the top of the stack.

Passing -q or --quiet to 'pppp'  or setting the environment variable
'PPPP_QUIET' suppresses all output except errors.

More help is available here:  https://github.com/rec/pppp

Command documentation:

""".format(
    icon=ICON,
    version=VERSION,
    first=', '.join(COMMANDS[:-1]),
    rest=COMMANDS[-1],
)


def pppp(*args):
    commands = []
    is_help = False
    is_quiet = QUIET
    for a in args:
        if a in ('--help', '-h'):
            is_help = True
        elif a in ('--quiet', '-q'):
            is_quiet = True
        else:
            commands.append(a)

    command = commands and commands.pop(0) or ''
    cmd = next((c for c in COMMANDS if c.startswith(command)), None)
    if is_help:
        return _help(command and cmd)

    projects = Projects(not is_quiet)

    if not command:
        return projects.cd()

    if _is_int(command):
        return projects.cd(command, *commands)

    p = _expand(command)
    if os.path.isdir(p):
        return projects.push(p, *commands)

    if '.' in command or '/' in command:
        _pexit('Directory', command, 'does not exist')

    if not cmd:
        _pexit('Do not understand command', command)

    method = getattr(projects, cmd)
    try:
        return method(*commands)
    except Exception as e:
        _pexit(e)


class Projects:
    def __init__(self, verbose):
        self._verbose = verbose
        self._config_file = '%s/%s' % (_expand(CONFIG_DIR), '.pppp.json')

        # self._projects is a stack, with the top element at 0.
        try:
            with open(str(self._config_file)) as fp:
                self._projects, self._undo = json.load(fp)
        except FileNotFoundError:
            self._projects, self._undo = [], []

        except Exception:
            _print('pppp: bad config file: ' + str(self._config_file))
            self._projects, self._undo = [], []

        self._original_projects = self._projects[:]

    def clear(self):
        """Clears the list of projects"""
        self._projects.clear()
        self._write()
        if self._verbose:
            _print('pppp: Cleared')
            _print()
            self.list()

    def cd(self, position=0):
        """Go right to a project at a specific position or by default the top
           project."""
        self._cd(position)

    def info(self):
        """Prints information about pppp itself"""
        _print('config_file:', self._config_file)
        _print('version:', VERSION)
        _print('branch:', _BRANCH)
        _print('commit_id:', _COMMIT_ID)
        _print('upstream:', _UPSTREAM)
        # _print('upstream_branch:', _UPSTREAM_BRANCH)

    def list(self):
        """Lists all the projects in order"""
        if not self._projects and self._verbose:
            _print('pppp: (no projects)')

        for i, p in enumerate(self._projects):
            _print('%d: %s' % (i, p))

    def pop(self, *positions):
        """Pop and discard a project"""
        if not self._projects:
            _pexit('pppp: ERROR: No projects to pop!')
        popped = []
        ps = {self._to_pos(p) for p in (positions or [0])}
        for position in reversed(sorted(ps)):
            p = self._projects.pop(position)
            popped.append(p)

        self._write()
        if self._projects and not position:
            self._cd(0, False)

        if self._verbose:
            _print('pppp: Popped', *popped)
            self.list()

    def push(self, *projects):
        """Push a project directory into the project list."""

        projects = [_expand(p) for p in projects]
        errors = []

        nonexistent = [p for p in projects if not os.path.exists(p)]
        if nonexistent:
            _print('pppp: Non-existent', *nonexistent)

        exists = [p for p in projects if os.path.exists(p)]
        not_dir = [p for p in exists if not os.path.isdir(p)]
        if not_dir:
            _print('pppp: Not a directory', *not_dir)

        if nonexistent or not_dir:
            _pexit('Failed')

        next_index = 0
        pushed = []
        for project in projects:
            project = str(project)
            try:
                index = self._projects.index(project)
            except Exception:
                self._projects.insert(0, project)
                next_index = 0
                pushed.append(project)
            else:
                if index:
                    self._projects.pop(index)
                    self._projects.insert(0, project)

                next_index = 0

        self._write()
        self._cd(next_index, False)
        if self._verbose:
            _print('pppp: Pushed', ', '.join(pushed))
            self.list()

    def rotate(self, steps=1):
        """Rotate the list of project directories in a cycle

           The default steps=1 rotates the current project to the bottom and
           brings the secondmost project to the top.

           Rotating by -1 undoes that exactly.  For convenience, you can just
           type 'pppp rotate -'."""
        steps = self._to_pos(steps)
        self._projects = self._projects[steps:] + self._projects[:steps]
        self._write()
        self._cd(0, False)
        if self._verbose:
            _print('pppp: rotated by', steps)
            self.list()

    def undo(self):
        """Undoes the previous change to the projects list"""
        self._projects = self._undo
        self._write()
        if self._verbose:
            _print('pppp: Undo!')
            _print()
            self.list()

    def swap(self):
        """Swap the top and second from top projects"""
        if len(self._projects) < 2:
            _pexit('Not enough directories to swap')
        self._projects[0:2] = reversed(self._projects[0:2])
        self._write()
        self._cd(0, False)
        if self._verbose:
            _print('pppp: swapped')
            self.list()

    def _cd(self, position, report=True):
        """Go right to a project at a specific position or by default the top
           project."""
        if not self._projects:
            self.list()
            return

        change = False
        if self._projects:
            next_project = self._projects[self._to_pos(position)]
            if next_project != _getcwd():
                print(next_project)
                change = True

        if self._verbose:
            if change:
                if report:
                    _print('pppp:', next_project)
            elif report:
                self.list()

    def _write(self):
        parent = os.path.dirname(self._config_file)
        os.makedirs(parent, exist_ok=True)
        output = json.dumps([self._projects, self._original_projects])
        with open(str(self._config_file), 'w') as fp:
            fp.write(output)

    def _to_pos(self, pos):
        if pos == '-':
            return -1
        try:
            pos = int(pos)
        except Exception:
            try:
                pos = self._projects.index(str(_expand(pos)))
            except Exception:
                _pexit('Cannot understand position', pos)

        lp = len(self._projects)
        if -lp <= pos < lp:
            return pos
        _pexit('Project index', pos, 'out of range [0, %d]' % (lp - 1))


# These are replaced by _write_pppp_bash.py
_COMMIT_ID = '{commit_id}'
_BRANCH = '{branch}'
_UPSTREAM_BRANCH = '{upstream_branch}'
_UPSTREAM = '{upstream}'


def _git(cmd):
    cmd = ['git'] + cmd.split()
    try:
        return subprocess.check_output(cmd).decode('utf-8').splitlines()
    except Exception as e:
        return []


def _expand(p):
    path = os.path.expandvars(p or _getcwd())
    return os.path.abspath(os.path.expanduser(path))


def _is_int(c):
    try:
        int(c)
        return True
    except Exception:
        return False


def _print(*args):
    print(*args, file=sys.stderr)


def _pexit(*args):
    _print('ERROR: pppp:', *args)
    sys.exit(-1)


def _help(command):
    if not command:
        _print(DESCRIPTION)
    for c in (command and [command]) or dir(Projects):
        if c.startswith('_'):
            continue

        try:
            method = getattr(Projects, c)
            sig = inspect.signature(method)
        except Exception:
            continue
        params = ['[%s]' % p for p in sig.parameters.values()][1:]
        _print('pppp', c, *params)
        for line in method.__doc__.splitlines():
            _print('   ', line.replace(11 * ' ', ''))
        _print()


def _getcwd():
    try:
        return os.getcwd()
    except Exception:
        return ''


if __name__ == '__main__':
    pppp(*sys.argv[1:])
