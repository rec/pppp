pppp : `pico push push project`
----------

``pppp`` is a tiny utility for Bash that does one thing well - it keeps a
stack of working directories across Bash shells and terminal sessions.

Like most people, I have many projects and subprojects working at once, and
often I get interrupted with bug reports, requests or even sudden inspiration,
and even get interrupted during interruptions, so I'm constantly moving between
multiple terminal windows and forgetting where I was.

This tiny utility saves me minutes a day, and never gets in my way.

Installation
---------------

Download the file
`pppp.sh <https://raw.githubusercontent.com/rec/pppp/master/pppp.sh>`_
and save it somewhere convenient.

Then in your .bashrc, add a line ``source /path/to/your/pppp.sh``
to define the Bash function ``pppp``.


``pppp`` Commands
-------------------

* ``pppp`` without arguments changes directory to the top of the stack
* ``pppp <dir>`` pushes ``<dir>`` on top of the stack
* ``pppp push`` or ``pppp p`` pushes the current directory on the stack
* ``pppp pop`` pops the top directory off the stack
* ``pppp pop <n>`` pops just the <n>th directory from the stack
* ``pppp list`` or ``pppp l`` lists the stack
* ``pppp clear`` clears it
* ``pppp swap`` or ``pppp s`` swaps the top and second directories
* ``pppp rotate`` or ``pppp r`` rotates the stack one step forward so the top is now
  at the bottom
* ``pppp rotate -1`` or ``pppp r -1`` rotates the stack one step backward bringing
  the bottom back to the top
* ``pppp undo`` or ``pppp u`` undoes the previous operation

With the exception of ``pppp list``, which has no side effects, each command
changes Bash's working directory to the top of the stack as it completes, unless
there's an error (like trying to push a non-existent directory).

If you want to jump back to the directory you were in before you typed ``pppp``,
use ``cd -``.


My ``pppp`` workflow
-------------------------------

* I alias ``pppp`` to ``p`` to avoid typing.

* When I switch to a terminal window or open a new one, I type ``p`` to go to my
  top project.

* When I get a new project I use ``p <dirname>`` to start work on it as my new
  top project, pushing the previous one down a level.

* Later I use ``p pop`` to go back to the previous project, if the new project
  is finished.

* Or if it is not, I use ``p r`` (rotate) to rotate the new project to the
  bottom and go back to the previous project.

* I use ``p pop -1`` to pop my oldest task, when I'm cleaning up clutter.

* When I'm working with two directories I push them both and then use ``p s``
  (swap) to move back and forth.

* And I use ``p u`` (undo) when I make a mistake.


FAQ:
-----------

Q: Why ``pppp``?

A: I was using it under the name ``p`` (for project) but ``pp`` and ``ppp``
were taken.

Q: What new features are expected?

A: None.  Barring bugfixes, I don't expect to change anything.

Q: Where does ``pppp`` store the the persistent stack?

A: By default, in the directory ``$HOME/.config/`` in the file file
``.pppp.json``.

Q: What if I want to change the directory for the config file?

A: Then set environment variable ``XDG_CONFIG_HOME``.

Q: Where did XDG come from?

A: `This specification
<https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
See also `this article <https://0x46.net/thoughts/2019/02/01/dotfile-madness/>`.

Q: Why is it Python code embedded in a Bash script?  Why not just distribute
a Python script?

A: A Bash script is needed in order to change the active directory in the shell
that you're working in, and I didn't want to distribute two files.
