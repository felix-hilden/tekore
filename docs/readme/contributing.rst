Issues
======
To file a bug report, ask about the package or voice any other concern,
please `submit <https://github.com/felix-hilden/spotipy/issues>`_ an issue.
We'll do our best to address each issue in a timely manner!

Contributing
============
If you'd like to get involved beyond creating issues,
please do submit a pull request for a fix or an enhancement!

Issues tagged ``consideration`` ought to be discussed further before implementation.
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_
is the canonical style guide for Python.
In addition, ``flake8`` and ``flake8-bugbear`` are great tools for code style.
See ``.travis.yml`` for the current style check.

Running tests
=============
The repository contains a suite of test cases
which can be studied and run to ensure the package works as intended.
To get up and running, clone the repository,
install it as an editable package and run the suite.

.. code:: sh

    $ git clone https://github.com/felix-hilden/spotipy.git
    $ cd spotipy
    $ pip install -e .[dev]
    $ python -m unittest discover tests -p "*.py"

Tests against the live Web API use environment variables for credentials.
These tests manipulate your data and player,
but try to restore previous state insofar as it is possible.
Please refer to the description of each test class for details.
In order to run all tests successfully, one must specify:

* ``SPOTIPY_CLIENT_ID`` - client ID of a registered Spotify 3rd party application
* ``SPOTIPY_CLIENT_SECRET`` - secret associated with that application
* ``SPOTIPY_REDIRECT_URI`` - redirect URI whitelisted in application settings
* ``SPOTIPY_USER_REFRESH`` - user refresh token with all scopes

In addition, playback tests require an active Spotify device
that does not have a private session enabled.
An empty song queue is also required, as the Web API does not implement
queue functionality, but skipping to the next song still consumes the queue.

Optionally ``SPOTIPY_TEST_SKIP_IS_FAIL`` can be set to raise an error if some
of the tests would be skipped because of the environment has not been configured.

To measure test coverage and view uncovered lines or branches run ``coverage``.

.. code:: sh

    $ coverage run --branch -m unittest discover tests -p "*.py"
    $ coverage report -m
