======
|logo|
======
|travis| |documentation| |coverage|

Welcome to the GitHub repository of Tekore,
a client of the Spotify Web API for Python!
Tekore allows you to interact with the Web API effortlessly.

.. code:: python

    from tekore import Spotify

    spotify = Spotify(token)

    tracks = spotify.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    spotify.playback_start_tracks([finlandia])

See our homepage on `PyPI`_ for more information
about the package and its versions.
Visit our online documentation on `Read The Docs`_ for tutorials,
examples, package reference and a detailed description of features.

Documentation
=============
Documentation can also be built locally.

.. code:: sh

    $ git clone https://github.com/felix-hilden/tekore.git
    $ cd tekore
    $ pip install -e .[dev]
    $ cd docs && make html

The main page ``index.html`` can be found in ``build/html``.

Issues
======
To file a bug report, ask about the package or voice any other concern,
please `submit <https://github.com/felix-hilden/tekore/issues>`_ an issue.
We'll do our best to address each one in a timely manner!

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

    $ git clone https://github.com/felix-hilden/tekore.git
    $ cd tekore
    $ pip install -e .[dev]
    $ python -m unittest discover tests -p "*.py"

Tests against the live Web API use environment variables for credentials.
These tests manipulate your data and player,
but try to restore previous state insofar as it is possible.
Please refer to the description of each test class for details.
In order to run all tests successfully, one must specify:

* ``SPOTIFY_CLIENT_ID`` - client ID of a registered Spotify 3rd party application
* ``SPOTIFY_CLIENT_SECRET`` - secret associated with that application
* ``SPOTIFY_REDIRECT_URI`` - redirect URI whitelisted in application settings
* ``SPOTIFY_USER_REFRESH`` - user refresh token with all scopes

In addition, playback tests require an active Spotify device
that does not have a private session enabled.
An empty song queue is also required, as the Web API does not implement
queue functionality, but skipping to the next song still consumes the queue.

Optionally ``TEKORE_TEST_SKIP_IS_FAIL`` can be set to raise an error if some
of the tests would be skipped because of the environment has not been configured.

To measure test coverage and view uncovered lines or branches run ``coverage``.

.. code:: sh

    $ coverage run --branch -m unittest discover tests -p "*.py"
    $ coverage report -m

.. |logo| image:: docs/logo_small.png
   :target: `pypi`_
   :alt: logo

.. |travis| image:: https://travis-ci.org/felix-hilden/tekore.svg?branch=master
   :target: https://travis-ci.org/felix-hilden/tekore
   :alt: build status

.. |documentation| image:: https://readthedocs.org/projects/tekore/badge/?version=latest
   :target: https://tekore.readthedocs.io/en/latest
   :alt: documentation status

.. |coverage| image:: https://api.codeclimate.com/v1/badges/627ab5f90253b59d4c8f/test_coverage
   :target: https://codeclimate.com/github/felix-hilden/tekore/test_coverage
   :alt: test coverage

.. _pypi: https://pypi.org/project/tekore
.. _web api: https://developer.spotify.com/documentation/web-api
.. _read the docs: https://tekore.readthedocs.io
