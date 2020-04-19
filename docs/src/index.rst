======
|logo|
======

Welcome to the online documentation of Tekore!
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
If you've found a bug or would like to propose a feature,
please submit an issue on `GitHub`_.
Join our `Discord <https://discord.gg/wcRXgJu>`_ community
to ask for help or discuss just about anything related to Tekore.

If you're new here, have a look at :ref:`getting-started`.
After your first calls to the API you might want to look at :ref:`advanced-usage`.
More ellaborate example scripts can be found in :ref:`examples`.
Detailed information can be found in our concise :ref:`reference`.

Features
========
The `Web API`_ provides access to a plethora of data on music and users.
Tekore implements these most integral features completely.

- :mod:`tekore.auth`: authentication for application and user tokens,
  self-refreshing tokens
- :mod:`tekore.client`: endpoints for access to every resource in the API.
  Responses are parsed into :mod:`models <tekore.model>` with explicit
  attributes to ease examining the contents of a response.

Additional features and various convenience modules are provided too.

- :mod:`tekore.util`

  - Command line prompt for user autentication
  - Read and write configuration from files and environment variables

- :mod:`tekore.sender`

  - Async support
  - Session persistence
  - Request retries
  - Response caching

- :mod:`tekore.convert` ID, URI and URL conversions
- :mod:`tekore.scope` Access right scopes for user tokens
- :mod:`tekore.serialise` Additional response model features

  - Readable ``repr``
  - JSON serialisation & dictionary conversion
  - Pretty-printing


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Package

   release_notes
   reference

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Guide

   getting_started
   advanced_usage
   examples
   extras

.. |logo| image:: logo.png
   :alt: logo
   :width: 432 px
   :target: `pypi`_

.. _pypi: https://pypi.org/project/tekore
.. _github: https://github.com/felix-hilden/tekore
.. _web api: https://developer.spotify.com/documentation/web-api
