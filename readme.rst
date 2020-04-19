======
|logo|
======
|travis| |documentation| |coverage|

Welcome to the GitHub repository of Tekore!
We provide a client for the Spotify Web API for Python,
complete with all available endpoints and authentication methods,
async support and loads of additional features.
Tekore allows you to interact with the API effortlessly.
Here's five lines to get you full access and start playing your top songs.

.. code:: python

    import tekore as tk

    conf = (client_id, client_secret, redirect_uri)
    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

    spotify = tk.Spotify(token)
    tracks = spotify.current_user_top_tracks(limit=10)
    spotify.playback_start_tracks([t.id for t in tracks.items])

See our homepage on `PyPI`_ for more information
about the package and its versions.
Visit our online documentation on `Read The Docs`_ for tutorials,
examples, package reference and a detailed description of features.
Join our `Discord <https://discord.gg/wcRXgJu>`_ community
to ask for help or discuss just about anything related to Tekore.

Contributing
============
|issues_open| |issue_resolution|

We welcome new contributors to Tekore!
If you've found a bug or would like to propose a feature,
please submit an `issue <https://github.com/felix-hilden/tekore/issues>`_.
Those that would like to get involved beyond that
can clone the repository and install it as an editable Python package.

.. code:: sh

    $ git clone https://github.com/felix-hilden/tekore.git
    $ cd tekore
    $ pip install -e .[dev]

Please have a look at the following sections for help in development.

Documentation
-------------
Documentation can be built locally with Sphinx.

.. code:: sh

    $ cd docs && make html

The main page ``index.html`` can be found in ``build/html/src``.

Running tests
-------------
The repository contains a suite of test cases
which can be studied and run to ensure the package works as intended.

.. code:: sh

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

Scripts
-------
Scripts for testing and linting can be found in the scripts folder.
They need to be executed from the top level folder.

.. code:: sh

    $ scripts/lint
    $ scripts/test

Windows users should use a batch wrapper to execute the files.

.. code:: batch

    > scripts\exec lint
    > scripts\exec test


.. |logo| image:: docs/src/logo_small.png
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

.. |issue_resolution| image:: http://isitmaintained.com/badge/resolution/felix-hilden/tekore.svg
   :target: https://isitmaintained.com/project/felix-hilden/tekore
   :alt: issue resolution time

.. |issues_open| image:: http://isitmaintained.com/badge/open/felix-hilden/tekore.svg
   :target: https://isitmaintained.com/project/felix-hilden/tekore
   :alt: open issues

.. _pypi: https://pypi.org/project/tekore
.. _web api: https://developer.spotify.com/documentation/web-api
.. _read the docs: https://tekore.readthedocs.io
