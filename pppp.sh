# In your .bashrc, source this file to add a bash function `pppp`.
# For more information, type `pppp -h` or `pppp --help`
#
# ------------------------------------------------------------------------
#
# Automatically generated on 2019-06-27 at 17:29:40 by _write_pppp_bash.py
# from file pppp.py

pppp() {
    DIR=`python - $@ <<'___EOF'

"""
Keep a persistent stack of working project directories
"""

from pathlib import Path
import inspect
import json
import os
import sys

DEFAULT_COMMAND = 'goto'
VERSION = '0.9.1'
DESCRIPTION = """pppp: Pico Push Pop Project v%s

A persistent stack of project directories you can push, pop, rotate, jump to a
position in, and list.

Very useful for people who get interrupted a lot.

-------------------------------------------------

Commands:

""" % VERSION


def pppp(*args):
    commands, hlp = [], []
    for a in args:
        (commands, hlp)[a in ('--help', '-h')].append(a)

    command = commands and commands.pop(0) or ''

    if command.startswith('_'):
        _pexit('Do not understand command', command)

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
            if m.startswith(command):
                command = m
                break
        else:
            p = Path(command)
            if not p.exists():
                _pexit('Do not understand command', command)

            # It's a filename
            commands = (command, *commands)
            command = 'push'

    if hlp:
        _help(command)
        return 0

    else:
        try:
            getattr(Projects(), command or DEFAULT_COMMAND)(*commands)
        except Exception as e:
            _pexit('Exception', e)


class Projects:
    def __init__(self):
        cf = os.environ.get('XDG_CONFIG_HOME', '$HOME/.config')
        config_dir = Path(os.path.expandvars(cf)).expanduser()
        self._config_file = config_dir / '.pppp.json'

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
        _perr('Cleared')
        _perr()
        self.list()

    def goto(self, position=0):
        """Go right to a project at a specific position or by default the top
           project."""
        print(self._projects and self._projects[self._to_pos(position)])

    def list(self):
        """Lists all the projects in order"""
        if not self._projects:
            _perr('(no projects)')

        for i, p in enumerate(self._projects):
            _perr('%d: %s' % (i, p))

    def pop(self, position=0):
        """Pop and discard a project"""
        if not self._projects:
            _pexit('No projects to pop!')

        _perr('Popped', self._projects.pop(self._to_pos(position)))
        self._write()
        self._projects and self.goto()
        self.list()

    def push(self, project=None):
        """Push a project directory into the project list.

           If no directory is specified, the current directory is used.
           """

        project = Path(os.path.expandvars(project or os.getcwd())).expanduser()
        if not project.exists():
            raise ValueError('Directory %s does not exist' % project)
        if not project.is_dir():
            raise ValueError('%s is not a directory' % project)
        project = str(project.absolute())
        if project in self._projects:
            raise ValueError('Cannot insert the same project twice')

        self._projects.insert(0, project)
        self._write()
        self.goto()

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
        self.list()

    def undo(self):
        """Undoes the previous change to the projects list"""
        self._projects = self._undo
        self._write()
        _perr('Undo!')
        _perr()
        self.list()

    def swap(self):
        """Swap the top and second from top projects"""
        if len(self._projects) < 2:
            raise ValueError('Not enough directories to swap')
        self._projects[0:2] = reversed(self._projects[0:2])
        self.list()

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
        raise IndexError('list index %d out of range' % pos)


def _perr(*args, **kwds):
    print(*args, **kwds, file=sys.stderr)


def _pexit(*args, **kwds):
    _perr(*args, **kwds)
    sys.exit(-1)


def _help(command):
    if not command:
        _perr(DESCRIPTION)
    for c in (command and [command]) or dir(Projects):
        if c.startswith('_'):
            continue

        try:
            method = getattr(Projects, c)
            sig = inspect.signature(method)
        except Exception:
            continue
        params = ['[%s]' % p for p in sig.parameters.values()][1:]
        _perr('pppp', c, *params)
        for line in method.__doc__.splitlines():
            _perr('   ', line.replace(11 * ' ', ''))
        _perr()


if __name__ == '__main__':
    pppp(*sys.argv[1:])

___EOF`

    if [ $DIR ] ; then
        cd $DIR
    fi
}
