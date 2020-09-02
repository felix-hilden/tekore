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
You can also ask a question on
`Stack Overflow <https://stackoverflow.com/questions/tagged/tekore>`_.

If you're new here, have a look at :ref:`getting-started`.
Example scripts can be found in :ref:`examples`.
Detailed information is available in our concise :ref:`reference`.

Features
========
The `Web API`_ provides access to a plethora of data on music and users.
Tekore implements these integral features completely.

- :ref:`auth` for applications and users.
- :ref:`Endpoints <client>` for access to every resource in the API.

Additional features are provided for your convenience.

- Support for :ref:`asynchronous programming <async>` using ``async/await``.
- A :ref:`self-refreshing <auth>` access token.
- Responses are parsed into :ref:`models <models>` with explicit attributes.
  They have a readable ``repr`` and can be serialised back to JSON.
- :ref:`senders`, a hook between Tekore and the Web API. Enables retries
  on failed requests, response caching and session persistence.
- :ref:`Access rights <auth-scopes>` for user tokens.
- :ref:`conversions` between Spotify IDs, URIs and URLs.
- Read and write :ref:`configuration <config>` from files and
  environment variables.


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
   auth_guide
   advanced_usage
   examples
   resources

.. |logo| image:: logo.png
   :alt: logo
   :width: 432 px
   :target: `pypi`_

.. _pypi: https://pypi.org/project/tekore
.. _github: https://github.com/felix-hilden/tekore
.. _web api: https://developer.spotify.com/documentation/web-api
