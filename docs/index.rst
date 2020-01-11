==============
|spotipy_logo|
==============

Welcome to the online documentation of Spotipy,
a client of the Spotify Web API for Python!
Spotipy allows you to interact with the Web API effortlessly.

.. code:: python

    from spotipy import Spotify

    spotify = Spotify(token)

    tracks = spotify.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    spotify.playback_start_tracks([finlandia])

See our homepage on `PyPI`_ for more information about the package,
and repository on `GitHub`_ if you'd like to submit an issue
or ask just about anything related to Spotipy.

If you're new here, have a look at :ref:`getting-started`.
After your first calls to the API you might want to look at :ref:`advanced-usage`.
More ellaborate example scripts can be found in :ref:`examples`.
Detailed information can be found in our concise :ref:`reference`.

Using an older version?
See the `legacy documentation <rtd old_>`_ for Spotipy 2.

Features
========
The `Web API`_ provides access to a plethora of data on music and users.
Spotipy implements these most integral features completely.

- :mod:`spotipy.auth`: authentication for application and user tokens,
  self-refreshing tokens
- :mod:`spotipy.client`: endpoints for access to every resource in the API.
  Responses are parsed into :mod:`models <spotipy.model>` with explicit
  attributes to ease examining the contents of a response.

Additional features and various convenience modules are provided too.

- :mod:`spotipy.util`

  - Command line prompt for user autentication
  - Read and write configuration from files and environment variables

- :mod:`spotipy.sender`

  - Session persistence
  - Request retries
  - Response caching
    (:ref:`possible <advanced-caching>` but not directly supported)

- :mod:`spotipy.convert` ID, URI and URL conversions
- :mod:`spotipy.scope` Access right scopes for user tokens
- :mod:`spotipy.serialise`

  - Response model serialisation
  - Response model pretty-printing


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Spotipy documentation

   documents/getting_started
   documents/advanced_usage
   examples
   reference

.. |spotipy_logo| image:: spotipy_logo.png
   :alt: spotipy logo
   :width: 275 px
   :target: `pypi`_

.. _pypi: https://github.com/felix-hilden/spotipy
.. _github: https://github.com/felix-hilden/spotipy
.. _rtd old: https://spotipy.readthedocs.io
.. _web api: https://developer.spotify.com/documentation/web-api
