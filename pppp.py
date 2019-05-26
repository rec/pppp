"""
Keeps a permanent stack of current project directories
"""

"""
Keep a stack of current projects - directories, essentially.

* go to
  * current project
  * project n

* rotate [default +1]
  * rotating by 1 means putting the current project at the back

* push a new project
  * at the top
  * at position n

* pop
  * the current project
  * project n

* undo the last operation

* list projects
"""

import inspect
import json
import os
import sys

CONFIG_ENV = '__PPPP_CONFIG'
DEFAULT_CONFIG = '~/.pppp.json'
CONFIG_FILE = os.path.expanduser(os.getenv(CONFIG_ENV, DEFAULT_CONFIG))


def pppp(*args):
    commands, hlp = [], []
    for a in args:
        (commands, hlp)[a in ('--help', '-h')].append(a)

    command = commands and commands.pop(0)
    if command and (command.startswith('_') or not hasattr(Projects, command)):
        _perr('Do not understand command', command)

    elif hlp:
        _help(command)

    else:
        getattr(Projects(), command)(*args)


class Projects:
    def __init__(self):
        # self.projects is a stack, with the top element at 0.
        try:
            with open(CONFIG_FILE) as fp:
                self.projects, self.undo = json.load(fp)
        except FileNotFoundError:
            self.projects, self.undo = [], []
        self.original_projects = self.projects[:]

    @property
    def project(self):
        return self.projects and self.projects[0]

    def goto(self, position=0):
        """Go right to a project at a specific position or by default the top
           project."""
        return (
            self.projects and self.projects[int(position) % len(self.projects)]
        )

    def rotate(self, steps=1):
        """Rotate the list of project directories in a cycle for one or more
           steps in either direction"""
        steps = int(steps) % len(self.projects)
        self.projects = self.projects[steps:] + self.projects[:steps]
        self._write()

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

        position = int(position)
        self.projects.insert(int(position), project)
        self._write()

    def pop(self, position=0):
        """Pop and discard a project - default 0 means the most recent one"""
        if self.projects:
            _perr('Popped', self.projects.pop(int(position)))
            self._write()

    def undo(self):
        """Undoes the previous change to the projects list"""
        self.projects = self.undo
        self._write()

    def clear(self):
        """Clears the list of projects"""
        self.projects.clear()
        self._write()

    def list(self):
        """Lists all the projects in order"""
        for i, p in enumerate(self.projects):
            _perr('%d: %s' % (i, p))

    def _write(self):
        with open(CONFIG_FILE, 'w') as fp:
            json.dump([self.projects, self.original_projects], fp)



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
        sig = (
            str(sig)
            .replace('(self', '')
            .replace(')', '')
            .replace(',', '')
        ).lstrip()
        _perr('pppp', c, sig)
        _perr('   ', method.__doc__)


if __name__ == '__main__':
    pppp(*sys.argv[1:])
