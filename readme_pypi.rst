|logo|

|python|

Welcome to the Python Package Index page of Tekore!
We provide a client for the Spotify Web API for Python,
complete with all available endpoints and authentication methods,
async support and loads of additional features.
Tekore allows you to interact with the API effortlessly.
Here's five lines to get you full access and start playing your top songs.

.. code:: python

    from tekore import Spotify, util, scope

    cred = (client_id, client_secret, redirect_uri)
    token = util.prompt_for_user_token(*cred, scope=scope.every)

    spotify = Spotify(token)
    tracks = spotify.current_user_top_tracks(limit=10)
    spotify.playback_start_tracks([t.id for t in tracks.items])

See our online documentation on `Read The Docs`_ for tutorials,
examples, package reference and a detailed description of features.
If you've found a bug or would like to propose a feature,
please submit an issue on `GitHub`_.
Join our `Discord <https://discord.gg/wcRXgJu>`_ community
to ask for help or discuss just about anything related to Tekore.

Installation
============
Tekore can be installed from the Package Index via ``pip``.

.. code:: sh

    $ pip install tekore

Versioning
==========
When requiring Tekore in projects or other packages,
please pin the version down to at least a specific major release
to avoid compatibility issues.
For example:

.. code:: python

    setup(
        install_requires=[
            'tekore>=1.1,<2'
        ]
    )

Tekore provides both stable and beta endpoints of the Web API.
However, beta endpoints may be changed by Spotify without prior notice,
so older versions of the library may have unintended issues.
Because of this, Tekore follows a modified form of
`Semantic Versioning <https://semver.org/>`_.
Incompatible changes in the library are still introduced in major versions,
and new features and endpoints are added in minor versions.
But endpoints removed by Spotify are removed in minor versions and changes
to endpoints are implemented as bugfixes.
See the Web API `documentation <web api_>`_ for further information on beta endpoints.

Changelog
=========
Unreleased
----------
Added
*****
- Endpoint for clearing playlist tracks

Fixed
*****
- ``playlist_tracks_add`` - fix insertion order when chunking (#156)

1.3.0 (2020-02-26)
------------------
Added
*****
- Endpoint for adding to queue
- Readable ``repr`` for response models
- Option to specify a maximum size for ``CachingSender``
- Optionally send long lists of resources as chunks

1.2.0 (2020-02-17)
------------------
Added
*****
- Optionally use maximum limits in all paging calls

Fixed
*****
- Retrieving all items and pages of a search respects API limits (#145)
- Always return an awaitable in paging navigation (#146)

1.1.0 (2020-02-02)
------------------
Added
*****
- Async support in authentication and API endpoints
- Sender that implements response caching
- Reading configuration with missing values produces a warning

Fixed
*****
- Correctly parse playlist when fields is specified (#142)

1.0.1 (2020-01-17)
------------------
Fixed
*****
- Accept missing video thumbnail in PlaylistTrack (#132)

1.0.0 (2020-01-14)
------------------
- Packaging improvements
- Declare versioning scheme

0.1.0 (2020-01-14)
------------------
Initial release of Tekore!


.. |logo| image:: https://raw.githubusercontent.com/felix-hilden/tekore/master/docs/logo_small.png
   :alt: logo

.. |python| image:: https://img.shields.io/pypi/pyversions/tekore
   :alt: python version

.. _github: https://github.com/felix-hilden/tekore
.. _read the docs: https://tekore.readthedocs.io
.. _web api: https://developer.spotify.com/documentation/web-api
