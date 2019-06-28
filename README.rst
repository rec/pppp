🍿 pppp: a tiny bash utility to manage project directories 🍿
--------------------------------------

Do you type ``cd`` a lot?

``pppp`` is a tiny utility for Bash that does one thing well - it keeps a
persistent stack of working directories across Bash shells and terminal
sessions.

Like many programmers, I have many projects and subprojects working at once, and
I often get interrupted with bug reports, requests or sudden inspiration, and
even get interrupted during interruptions, so I'm constantly moving between
multiple terminal windows and forgetting where I was.

``pppp`` saves me minutes a day, reminds of where I was when I get interrupted,
and never gets in my way.

Installation
---------------

Download the file
`pppp.sh <https://raw.githubusercontent.com/rec/pppp/master/pppp.sh>`_
and save it somewhere convenient.

Then in your .bashrc, add a line ``source /path/to/your/pppp.sh`` to define the
Bash function ``pppp``. I am lazy and add an alias ``alias p=pppp`` to avoid
typing.


``pppp`` Commands
-------------------

Commands can be abbreviated down to a single character, so ``pppp rotate``,
``pppp rot`` and ``pppp r`` all mean the same thing.

"cd" is short for "change the current working directory in the shell".

Push
==========
* ``pppp <directory>``: Push ``<directory>`` onto the stack and cd to it
* ``pppp push <directory>``: (Same)


Pop
==========
* ``pppp pop``: Pop the top directory off the stack and cd to the new top
* ``pppp pop <n>``: Pop the <n>th directory, but do not cd


Housekeeping: list, clear, undo
==================================
* ``pppp list``: Lists the stack
* ``pppp clear``: Clears the stack
* ``pppp undo``: Undoes the previous change to the stack and cds to the top of it


Change directory
==================

These commands don't change the stack, only the current directory

* ``pppp``: cd to the top of the stack. By far the most commonly used command.
* ``pppp 0``: (Same)
* ``pppp 1``: cd to the first directory below the top of the stack
* ``pppp 2``: cd to the second directory below the top of the stack
* ``pppp <n>``: cd to the nth directory below the top of the stack
* ``pppp -1``: cd to the directory at the bottom of the stack
* ``pppp -2``: cd to the directory one above the bottom of the stack
* ``pppp -<n>``: cd to the directory n-1 above the bottom of the stack


Reorder
==================

These commands change the stack, and then cd to its top

* ``pppp swap``: Swaps the top two directories
* ``pppp rotate``: Rotates the stack one step so the top moves to the bottom
* ``pppp rotate 1``: (Same)
* ``pppp rotate 1``: Rotates the stack two steps forward
* ``pppp rotate -1``: Rotates the stack one step backward
* ``pppp rotate -``: (Same)
* ``pppp rotate -1``: Rotates the stack two steps backward
* ``pppp rotate 0``: (Does nothing)

If you want to jump back to the directory you were in before you typed ``pppp``,
use ``cd -``.

By default, ``pppp``: prints what it has done, and prints the whole stack every
time it changes.  You can disable that by either passing in the
``-q``/``--quiet`` flag, or setting the ``PPPP_QUIET`` environment variable.


My ``pppp`` workflow
-------------------------------

* I alias ``pppp`` to ``p`` to avoid typing.

* When I switch to a terminal window or open a new one, I type ``p`` to cd to my
  top project.

* When I get a new project I use ``p <dirname>`` to start work on it as my new
  top project, pushing the previous one down a level.

* Later I use ``p p`` (pop) to cd back to the previous project, if the new project
  is finished.

* Or if it is not, I use ``p r`` (rotate) to rotate the new project to the
  bottom and cd back to the previous project.

* I use ``p p -1`` (pop) to pop my oldest task, when I'm cleaning up clutter.

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
