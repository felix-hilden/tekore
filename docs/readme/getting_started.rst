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
