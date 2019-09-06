==============
|spotipy_logo|
==============
|travis|

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
Until then the repository must be cloned and installed as a local package.

.. code:: sh

    $ git clone https://github.com/felix-hilden/spotipy.git
    $ cd spotipy
    $ pip install .

Retrieving an access token
--------------------------
First we'll retrieve an access token that has every possible right (scope)
to a user's account.
The script will open a web page prompting for a Spotify login.
If successful, the client will be redirected to the specified address
along with a code to request the token with.

.. code:: python

    import webbrowser
    from spotipy import Credentials, scopes, Scope

    client_id = 'yourtokenhere'
    client_secret = 'yoursecrethere'
    redirect_uri = 'http://localhost:5000'

    c = Credentials(client_id, client_secret, redirect_uri)
    scope = Scope(*scopes)

    url = c.authorisation_url(scope)
    webbrowser.open(url)
    code = input('Paste value of code: ')
    token = c.request_access_token(code, scope)

Calling the API
---------------
Next the Spotify object should be created.
An access token can be provided at initialisation.
Otherwise the context manager ``Spotify.token`` can be used.

The script below will play Sibelius' Finlandia if the user has
an active (recently used) Spotify application open.
If no active device is found, an error is thrown.
To change device state ``Spotify.playback_transfer`` can be used.

.. code:: python

    from spotipy import Spotify

    s = Spotify(token.access_token)

    finlandia = 'spotify:track:3hHWhvw2hjwfngWcFjIzqr'
    s.playback_start(uris=[finlandia])

Contributing
============
Contributions are welcome!

Issues
------
Please submit any issues or questions to the GitHub repository
`here <https://github.com/felix-hilden/spotipy/issues>`_.

Submitting code
---------------
Direct contributions are encouraged!
Issues tagged ``consideration`` ought to be discussed further
before implementation.
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_
is the canonical style guide for Python.

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
| Authorisation           | X                    | X               |
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
| Model-based API         | / (**)               |                 |
+-------------------------+----------------------+-----------------+

(*) Retries implemented for GET requests

(**) Response objects are implemented, but not yet returned from calls


.. |travis| image:: https://travis-ci.org/felix-hilden/spotipy.svg?branch=master

.. |spotipy_logo| image:: docs/spotipy_logo_small.png
   :alt: spotipy logo
   :target: https://github.com/felix-hilden/spotipy
