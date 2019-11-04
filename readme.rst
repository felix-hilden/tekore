==============
|spotipy_logo|
==============
|travis| |coverage|

A Python library for the Spotify `Web API`_.
See also `Contributing`_ and available `Features`_.

.. TODO: Keep duplicating content until inclusion in GitHub READMEs is resolved
   which is most probably forever as the issue was opened in 2012.
   There are several duplicates and the github/markup repository is not used
   in rendering, only determining which markup library to use :(
   https://github.com/github/markup/issues/172
   https://github.com/github/markup/issues/346

Getting started
===============
To use the Web API, you'll need to
`register <https://developer.spotify.com/dashboard/applications>`_
an application,
get its credentials and define a redirect URI for authentication requests.
Note that a server listening to that address isn't required for a demo,
though it is required for programmatic extraction of user access tokens.

Installation
------------
The package is not yet in PyPI.
Until then the repository must be installed via git.

.. code:: sh

    $ pip install git+https://github.com/felix-hilden/spotipy.git

Documentation
-------------
Modules, classes and functions are documented in the source code.
For a condensed and organised view, additional examples and other documents,
documentation can be built locally.

.. code:: sh

    $ git clone https://github.com/felix-hilden/spotipy.git
    $ cd spotipy
    $ pip install -e .[dev]
    $ cd docs && make html

The main page ``index.html`` can be found in ``build/html``.

Retrieving an access token
--------------------------
First we'll retrieve an access token that has every possible right (scope)
to a user's account.
The script will open a web page prompting for a Spotify login.
The user is then redirected back and the URL of the redirect is requested
for parsing and retrieving the access token.

.. code:: python

    from spotipy.scope import every
    from spotipy.util import prompt_for_user_token

    client_id = 'your_token_here'
    client_secret = 'your_secret_here'
    redirect_uri = 'http://localhost'

    token = prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=every
    )

Calling the API
---------------
Next the Spotify object should be created.
The following script will list some of the user's top tracks.

.. code:: python

    from spotipy import Spotify

    s = Spotify(token)

    tracks = s.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

The snippet below will play Sibelius' Finlandia if the user has
an active (recently used) Spotify application open.
If no active device is found, an error is thrown.

.. code:: python

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    s.playback_start(track_ids=[finlandia])

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

Features
========
The `Web API`_ provides access to a plethora of data on music and users.
Spotipy implements these most integral features completely.

- Authentication: client credentials (application token)
  and authorisation code (user token) flows according to the OAuth2 specification.
- API endpoints: access to every resource in the API.
  Responses are parsed into model classes with explicit
  attributes to ease examining the contents of a response.

Additional features and various convenience modules are provided too.
Please refer to the documentation of each module for more information.

- Request retries
- Session persistence
- Response caching (possible, though not directly supported)
- ID, URI and URL conversions
- Access right scopes
- Response serialisation
- Response pretty-printing
- Self-refreshing tokens
- Credentials from environment variables
- Command line prompt for user autentication


.. |travis| image:: https://travis-ci.org/felix-hilden/spotipy.svg?branch=master
   :target: https://travis-ci.org/felix-hilden/spotipy
   :alt: build status

.. |coverage| image:: https://api.codeclimate.com/v1/badges/6cbb70d77e31c4d3b4c6/test_coverage
   :target: https://codeclimate.com/github/felix-hilden/spotipy/test_coverage
   :alt: test coverage

.. |spotipy_logo| image:: docs/spotipy_logo_small.png
   :alt: spotipy logo
   :target: `github`_

.. _github: https://github.com/felix-hilden/spotipy
.. _web api: https://developer.spotify.com/documentation/web-api
