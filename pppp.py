"""
Keeps a permanent stack of current project directories
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
        _perr('Do not understand command', command)
        return

    if command.isnumeric():
        commands = command, *commands
        command = 'goto'

    if command:
        for m in dir(Projects):
            if m.startswith(command):
                command = m
                break
        else:
            _perr('Do not understand command', command)
            return

    if hlp:
        _help(command)

    else:
        try:
            result = getattr(Projects(), command or DEFAULT_COMMAND)(*commands)
        except Exception as e:
            _perr('ERROR', e)
            result = None
        print(result or os.getcwd())


class Projects:
    def __init__(self):
        # self.projects is a stack, with the top element at 0.
        try:
            with open(CONFIG_FILE) as fp:
                self.projects, self.undo = json.load(fp)
        except FileNotFoundError:
            self.projects, self.undo = [], []
        self.original_projects = self.projects[:]

    def goto(self, position=0):
        """Go right to a project at a specific position or by default the top
           project."""
        return self.projects and self.projects[self._to_pos(position)]

    def rotate(self, steps=1):
        """Rotate the list of project directories in a cycle for one or more
           steps in either direction"""
        steps = self._to_pos(steps)
        self.projects = self.projects[steps:] + self.projects[:steps]
        self._write()
        return self.goto()

    def push(self, project=None, position=0):
        """Push a project directory into the project list.

           If no directory is specified, the current directory is used.
           If no position is specified, it is pushed at the top.
           """
        project = os.path.abspath(
            os.path.expanduser(os.path.expandvars(project or os.getcwd()))
        )
        if project in self.projects:
            raise ValueError('Cannot insert the same project twice')

        self.projects.insert(self._to_pos(position), project)
        self._write()
        return self.goto()

    def pop(self, position=0):
        """Pop and discard a project - default 0 means the most recent one"""
        if self.projects:
            _perr('Popped', self.projects.pop(self._to_pos(position)))
            self._write()
            self.goto()

    def undo(self):
        """Undoes the previous change to the projects list"""
        self.projects = self.undo
        self._write()

    def clear(self):
        """Clears the list of projects"""
        self.projects.clear()
        self._write()
        self.list()

    def list(self):
        """Lists all the projects in order"""
        if not self.projects:
            _perr('(no projects)')

        for i, p in enumerate(self.projects):
            _perr('%d: %s' % (i, p))

    def _write(self):
        with open(CONFIG_FILE, 'w') as fp:
            json.dump([self.projects, self.original_projects], fp)

    def _to_pos(self, pos):
        return (int(pos) % len(self.projects)) if self.projects else 0



def _perr(*args, **kwds):
    print(*args, **kwds, file=sys.stderr)


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
