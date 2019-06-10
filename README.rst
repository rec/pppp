pppp : `pico push push project`
----------

``pppp`` is a tiny utility for Bash that does one thing well - it keeps a
stack of working directories across Bash shells.

Like most programmers, I have many projects and subprojects working at once, and
often I get interrupted with bug reports, requests or even sudden inspiration,
and even get interrupted during interruptions, moving between multiple terminal
windows and occasionally typing a command in a wrong window.

Installation
---------------

Download the file ``pppp.sh``, and in your .bashrc, execute ``source pppp.sh``
which adds an alias ``pppp``.


Commands
---------
I alias it to just ``p``.

* ``p`` without arguments changes directory to the top of the stack
* ``p <dir>`` pushes ``<dir>`` on top of the stack
* ``p push`` or ``p p`` pushes the current directory on the stack
* ``p pop`` pops the top directory off the stack
* ``p pop 3`` pops the third directory from inside the stack
* ``p list`` or ``p l`` lists the stack
* ``p clear`` clears it
* ``p swap`` or ``p s`` swaps the top and second directories
* ``p rotate`` or ``p r`` rotates the stack one step so the top is now at the
  bottom
* ``p rotate -1`` or ``p r -1`` rotates it one step in reverse bringing the
  bottom back to the top
* ``p undo`` or ``p u`` undoes the previous operation

With the exception of ``p list``, which has no side effects, each command
changes directory to the top of the stack as it completes.


How I use ``pppp``
-------------------------------

``pppp`` saves me a lot of work and forgetting by keeping a stack of the
directories I am working on.

* When I get a new request or task I use ``p <dirname>`` to start work on it.

* When I switch to a terminal window, I type ``p`` to go to my current project.

* I use ``p pop`` to go back to my previous task, if this task is finished, or
  ``p r`` (rotate) to rotate the project to the bottom if I'm waiting for
  something to complete it

* When I'm working with two directories I push them both and then use ``p s``
  (swap).


FAQ:

Q: Why ``pppp``?

A: I was using it under the name ``p`` (for project( but ``pp`` and ``ppp``
are just too common.

Q: What new features are expected?

A: None.  Barring bugfixes, I don't expect to change anything.

Q: Where does it store the project data?
