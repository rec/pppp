# In your .bashrc, source this file to add a bash function `pppp`.
#
# For more information, type `pppp -h` or `pppp --help`
#
# ------------------------------------------------------------------------
#
# Automatically generated on 2019-06-28 at 11:57:08 by _write_pppp_bash.py
# from file pppp.py

pppp() {
    DIR=`python - $@ <<'___EOF'

"""

pppp: Pico Push Pop Project

Keep a persistent stack of working project directories
"""

from pathlib import Path
import inspect
import json
import os
import sys

PPPP_QUIET_ENV = 'PPPP_QUIET'
QUIET = os.environ.get(PPPP_QUIET_ENV, '')
CONFIG_DIR = os.environ.get('XDG_CONFIG_HOME', '$HOME/.config')

DEFAULT_COMMAND = 'goto'
VERSION = '0.9.1'
DESCRIPTION = """pppp: Pico Push Pop Project v%s

A persistent stack of project directories you can push, pop, rotate, jump to a
position in, and list.

Very useful for people who get interrupted a lot.

-------------------------------------------------

By default, pppp prints the contents of its stack after each operation.
To turn this off, either set the environment variable PPPP_QUIET, or
pass the -q or --quiet flag to the program.

Commands:

""" % VERSION


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

    if command.isnumeric():
        # Go to a specific position
        commands = (command, *commands)
        command = 'goto'

    elif '.' in command or '/' in command:
        # It's a filename you want to push
        commands = (command, *commands)
        command = 'push'

    elif command == 'p':
        # Disambiguate 'p' as 'push' and not 'pop'
        command = 'push'

    if command:
        for m in dir(Projects):
            if m.startswith(command) and not command.startswith('_'):
                command = m
                break
        else:
            p = Path(command)
            if p.exists():
                # It's a filename
                commands = (command, *commands)
                command = 'push'
            else:
                _pexit('Do not understand command', command)

    if is_help:
        _help(command)
    else:
        try:
            projects = Projects(not is_quiet)
            getattr(projects, command or DEFAULT_COMMAND)(*commands)
        except Exception as e:
            _pexit('pppp: ERROR:', e)


class Projects:
    def __init__(self, verbose):
        self._verbose = verbose
        cf = os.environ.get('XDG_CONFIG_HOME', '$HOME/.config')
        self._config_file = _expand(CONFIG_DIR) / '.pppp.json'

        # self._projects is a stack, with the top element at 0.
        try:
            with open(str(self._config_file)) as fp:
                self._projects, self._undo = json.load(fp)
        except FileNotFoundError:
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

    def goto(self, position=0):
        """Go right to a project at a specific position or by default the top
           project."""
        self._goto(position)

    def list(self):
        """Lists all the projects in order"""
        if not self._projects:
            if self._verbose:
                _print('pppp: (no projects)')

        for i, p in enumerate(self._projects):
            _print('%d: %s' % (i, p))

    def pop(self, position=0):
        """Pop and discard a project"""
        if not self._projects:
            _pexit('pppp: ERROR: No projects to pop!')

        popped = self._projects.pop(self._to_pos(position))
        self._write()
        if self._projects and not position:
            self._goto(0, False)

        if self._verbose:
            _print('pppp: Popped', popped)
            self.list()

    def push(self, project=None):
        """Push a project directory into the project list.

           If no directory is specified, the current directory is used."""
        project = _expand(project)
        if not project.exists():
            raise ValueError('Directory %s does not exist' % project)
        if not project.is_dir():
            raise ValueError('%s is not a directory' % project)
        project = str(project)
        if project in self._projects:
            raise ValueError('Cannot insert the same project twice')

        self._projects.insert(0, project)
        self._write()
        self._goto(0, False)
        if self._verbose:
            _print('pppp: Pushed', project)
            self.list()

    def rotate(self, steps=1):
        """Rotate the list of project directories in a cycle

           The default steps=1 rotates the current project to the bottom and
           brings the secondmost project to the top.

           Rotating by -1 undoes that exactly.  For convenience, you can just
           type 'pppp rotate -'.
        """
        steps = self._to_pos(steps)
        self._projects = self._projects[steps:] + self._projects[:steps]
        self._write()
        self.goto()
        if self._verbose:
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
            raise ValueError('Not enough directories to swap')
        self._projects[0:2] = reversed(self._projects[0:2])

    def _goto(self, position, report=True):
        """Go right to a project at a specific position or by default the top
           project."""
        change = False
        if self._projects:
            next_project = self._projects[self._to_pos(position)]
            if next_project != os.getcwd():
                print(next_project)
                change = True

        if self._verbose:
            if change:
                if report:
                    _print('pppp:', next_project)
            elif report:
                _print('pppp: (no change)')

    def _write(self):
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(str(self._config_file), 'w') as fp:
            json.dump([self._projects, self._original_projects], fp)

    def _to_pos(self, pos):
        if pos == '-':
            return -1
        pos, lp = int(pos), len(self._projects)
        if -lp <= pos < lp:
            return pos
        raise IndexError(
            'Project index %d out of range [0, %d]' % (pos, lp -1)
        )


def _expand(p):
    return Path(os.path.expandvars(p or os.getcwd())).expanduser().absolute()


def _print(*args):
    print(*args, file=sys.stderr)


def _pexit(*args):
    _print(*args)
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


if __name__ == '__main__':
    pppp(*sys.argv[1:])

___EOF`

    if [ $DIR ] ; then
        cd $DIR
    fi
}
