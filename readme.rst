==============
|spotipy_logo|
==============
|travis| |coverage|

A Python library for the
`Spotify Web API <https://developer.spotify.com/documentation/web-api/>`_.
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

Contributing
============
Contributions are welcome!

Issues
------
Please submit any issues or questions to the GitHub repository
`here <https://github.com/felix-hilden/spotipy/issues>`_.

Tests
-----
To get up and running, clone the repository,
install it as an editable package and run tests.

.. code:: sh

    $ git clone https://github.com/felix-hilden/spotipy.git
    $ cd spotipy
    $ pip install -e .[dev]
    $ python -m unittest discover tests -p "*.py"

Tests for the Web API client use environment variables for credentials.
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

To measure test coverage and view uncovered lines or branches run ``coverage``.

.. code:: sh

    $ coverage run --branch -m unittest discover tests -p "*.py"
    $ coverage report -m

Submitting code
---------------
Direct contributions are encouraged!
Issues tagged ``consideration`` ought to be discussed further
before implementation.
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_
is the canonical style guide for Python.
In addition, ``flake8`` and ``flake8-bugbear`` are a great addition.
See ``.travis.yml`` for the current style check.


Features
========
Spotipy replaces `plamere/spotipy <https://github.com/plamere/spotipy>`_,
which has not been maintained since the end of 2017.
Although refactored heavily from its original source, this package does
rely on the original structure that was put in place by plamere.

The equivalent functionality of the original Spotipy is already implemented.
Some additional features are also provided and being developed.
Below ``X`` indicates a complete feature and ``/`` an incomplete one.

Basic features
--------------
+-------------------------+----------------------+-----------------+
| Spotify Web API feature | felix-hilden/spotipy | plamere/spotipy |
+=========================+======================+=================+
| Authentication          | X                    | X               |
+-------------------------+----------------------+-----------------+
| Endpoints               | X                    | / (*)           |
+-------------------------+----------------------+-----------------+
| Conditional requests    | (**)                 |                 |
+-------------------------+----------------------+-----------------+

(*) Not all endpoints are implemented

(**) While not directly supported,
they are made possible by creating custom ``Sender`` classes.
See documentation on advanced usage for further details.

Additional features
-------------------
+-------------------------+----------------------+-----------------+
| Feature                 | felix-hilden/spotipy | plamere/spotipy |
+=========================+======================+=================+
| Request retries         | X                    | / (*)           |
+-------------------------+----------------------+-----------------+
| Auto-refreshing token   | X                    |                 |
+-------------------------+----------------------+-----------------+
| Model-based API         | X                    |                 |
+-------------------------+----------------------+-----------------+

(*) Retries implemented for GET requests


.. |travis| image:: https://travis-ci.org/felix-hilden/spotipy.svg?branch=master
   :target: https://travis-ci.org/felix-hilden/spotipy
   :alt: build status

.. |coverage| image:: https://api.codeclimate.com/v1/badges/6cbb70d77e31c4d3b4c6/test_coverage
   :target: https://codeclimate.com/github/felix-hilden/spotipy/test_coverage
   :alt: test coverage

.. |spotipy_logo| image:: docs/spotipy_logo_small.png
   :alt: spotipy logo
   :target: https://github.com/felix-hilden/spotipy
