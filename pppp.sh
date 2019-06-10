pppp() {
    DIR=`python - $@ <<'___EOF'
"""
Keep a persistent stack of working project directories
"""

import inspect
import json
import os
import sys

CONFIG_ENV = '__PPPP_CONFIG'
DEFAULT_CONFIG = '~/.pppp.json'
CONFIG_FILE = os.path.expanduser(os.getenv(CONFIG_ENV, DEFAULT_CONFIG))
DEFAULT_COMMAND = 'goto'


def pppp(*args):
    commands, hlp = [], []
    for a in args:
        (commands, hlp)[a in ('--help', '-h')].append(a)

    command = commands and commands.pop(0) or ''

    if command.startswith('_'):
        _pexit('Do not understand command', command)

    if command.isnumeric():
        # Go to a specific position
        commands = command, *commands
        command = 'goto'

    elif '.' in command or '/' in command:
        # It's a filename you want to push
        commands = command, *commands
        command = 'push'

    elif command == 'p':
        # Disambiguate between 'push' and 'pop'
        command = 'push'

    if command:
        for m in dir(Projects):
            if m.startswith(command):
                command = m
                break
        else:
            _pexit('Do not understand command', command)

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
        # self._projects is a stack, with the top element at 0.
        try:
            with open(CONFIG_FILE) as fp:
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
        """Pop and discard a project - default 0 means the most recent one"""
        if self._projects:
            _perr('Popped', self._projects.pop(self._to_pos(position)))
            self._write()
            self.goto()

    def push(self, project=None, position=0):
        """Push a project directory into the project list.

           If no directory is specified, the current directory is used.
           If no position is specified, it is pushed at the top.
           """
        project = os.path.abspath(
            os.path.expanduser(os.path.expandvars(project or os.getcwd()))
        )
        if project in self._projects:
            raise ValueError('Cannot insert the same project twice')

        self._projects.insert(self._to_pos(position), project)
        self._write()
        self.goto()

    def rotate(self, steps=1):
        """Rotate the list of project directories in a cycle for one or
           more steps in either direction.  For convenience, you can say
           'rotate -' to mean 'rotate -1' - to undo the previous rotation.
        """
        steps = self._to_pos(steps)
        self._projects = self._projects[steps:] + self._projects[:steps]
        self._write()
        self.goto()

    def undo(self):
        """Undoes the previous change to the projects list"""
        self._projects = self._undo
        self._write()
        _perr('Undo!')
        _perr()
        self.list()

    def _write(self):
        with open(CONFIG_FILE, 'w') as fp:
            json.dump([self._projects, self._original_projects], fp)

    def _to_pos(self, pos):
        pos = -1 if pos == '-' else int(pos)
        return (int(pos) % len(self._projects)) if self._projects else 0


def _perr(*args, **kwds):
    print(*args, **kwds, file=sys.stderr)


def _pexit(*args, **kwds):
    _perr(*args, **kwds)
    sys.exit(-1)


def _help(command):
    for c in (command and [command]) or dir(Projects):
        if c.startswith('_'):
            continue

        try:
            method = getattr(Projects, c)
            sig = inspect.signature(method)
        except Exception:
            continue
        params = [str(p) for p in sig.parameters.values()][1:]
        _perr('pppp', c, *params)
        for line in method.__doc__.splitlines():
            _perr('   ', line.replace(11 * ' ', ''))
        _perr()


if __name__ == '__main__':
    pppp(*sys.argv[1:])

___EOF`
    if [ $DIR ] ; then
        echo "--> $DIR"
        cd $DIR
    fi
}
