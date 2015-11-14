================
 nose-blacklist
================

nose-blacklist is a plugin for nose_ that provides a powerful way of skipping
tests without requiring code changes.

Features:

- Test cases are excluded by regex matching
- Test modules, classes, and functions can be matched
- Tests to skip can be sourced from one or more files, or from cli arguments


Quickstart
==========

.. code-block:: python

    $ pip install nose-blacklist

    $ nosetests --with-blacklist \
        --blacklist=<pattern1> \
        --blacklist=<pattern2> \
        mytests/

Blacklist strings can be specified from one or more files. Blacklist files can
be used in conjunction with the ``--blacklist`` arguments.

    $ cat blacklist.txt
    test_thing
    # test_other_thing
    test_third_thing

    $ nosetests --with-blacklist \
        --blacklist-file=blacklist.txt \
        mytests/

The blacklist file should have a single pattern per line, as above. Any line
starting with a ``#`` is commented and will be ignored.


.. _nose: https://nose.readthedocs.org/en/latest/
