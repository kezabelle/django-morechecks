=================
django-morechecks
=================

Because Django 1.7 has a new checks framework, but only for things that
*would prevent startup or cause known problems.*

This is me implementing others, as I need them.

Checks
------

* ``morechecks.checks.templates_do_not_do_queries`` - Ensures that any custom
  context processors do not trigger a query just by being used. They should
  instead be made lazy, such that the database is hit when the context variable
  is *used*.

That's it, so far.

Usage
-----

Add ``morechecks`` to your ``INSTALLED_APPS`` and run::

    python manage.py check morechecks
