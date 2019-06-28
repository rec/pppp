🍿 pppp: a tiny bash utility to manage project directories 🍿
--------------------------------------

``pppp`` is a tiny utility for Bash that does one thing well - it keeps a
persistent stack of working directories across Bash shells and terminal
sessions.

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
* ``pppp #`` where # is a number goes to that
* ``pppp <dir>`` pushes ``<dir>`` on top of the stack
* ``pppp pop`` pops the top directory off the stack
* ``pppp pop <n>`` pops just the <n>th directory from the stack
* ``pppp list`` or ``pppp l`` lists the stack
* ``pppp clear`` clears it
* ``pppp swap`` or ``pppp s`` swaps the top and second directories
* ``pppp rotate`` or ``pppp r`` rotates the stack one step forward so the top is
  now at the bottom
* ``pppp rotate -1`` or ``pppp r -`` rotates the stack one step backward
  bringing the bottom back to the top
* ``pppp undo`` or ``pppp u`` undoes the previous operation

With the exception of ``pppp list``, which has no side effects, each command
changes Bash's working directory to the top of the stack as it completes, unless
there's an error (like trying to push a non-existent directory).

If you want to jump back to the directory you were in before you typed ``pppp``,
use ``cd -``.

By default, ``pppp`` prints what it has done, and prints the whole stack every
time it changes.  You can disable that by either passing in the
``-q``/``--quiet`` flag, or setting the ``PPPP_QUIET`` environment variable.


My ``pppp`` workflow
-------------------------------

* I alias ``pppp`` to ``p`` to avoid typing.

* When I switch to a terminal window or open a new one, I type ``p`` to go to my
  top project.

* When I get a new project I use ``p <dirname>`` to start work on it as my new
  top project, pushing the previous one down a level.

* Later I use ``p p`` (pop) to go back to the previous project, if the new project
  is finished.

* Or if it is not, I use ``p r`` (rotate) to rotate the new project to the
  bottom and go back to the previous project.

* I use ``p p -1`` to pop my oldest task, when I'm cleaning up clutter.

* When I'm working with two directories I push them both and then use ``p s``
  (swap) to move back and forth.

* And I use ``p u`` (undo) when I make a mistake.


FAQ:
-----------

Q: Why ``pppp``?

A: It's a Project to Push and Pop other Projects.  Also, I use ``p`` as a
shortcut but ``p``, ``pp``, and ``ppp`` are too short or already taken.

Q: What new features are expected?

A: None.  Barring bugfixes, I don't expect to change anything.  I am open to
ideas but it feels complete to me.

Q: Where does ``pppp`` store the the persistent stack?

A: By default, in the directory ``$HOME/.config/`` in the file file
``.pppp.json``.

Q: What if I want to change the directory for the config file?

A: Set the environment variable ``XDG_CONFIG_HOME`` to your directory.

Q: What's this XDG thing?

A: `This specification
<https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_
for where your config files should go.

See also `this article <https://0x46.net/thoughts/2019/02/01/dotfile-madness/>`.

Q: Why is there Python code embedded in a Bash script?  Why the Makefile and the
build step?  Why not just distribute a Python script?

A: Pure Python cannot change the directory in your shell - some Bash is needed.
But doing the whole thing in Bash was too hard.

I could have distributed it as a Python file and a small Bash file but I felt a
single file was better for everyone, even though it requires a build step (for
developers only of course).

See also `this discussion
<https://stackoverflow.com/questions/2375003/how-do-i-set-the-working-directory-of-the-parent-process>`_
which seems to show that no better way is possible.
