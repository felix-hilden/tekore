|logo|

|python| |downloads|

Welcome to the Python Package Index page of Tekore!
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

See our online documentation on `Read The Docs`_ for tutorials,
examples, package reference and a detailed description of features.
If you've found a bug or would like to propose a feature,
please submit an issue on `GitHub`_.
Join our `Discord <https://discord.gg/wcRXgJu>`_ community
to ask for help or discuss just about anything related to Tekore.
You can also ask a question on
`Stack Overflow <https://stackoverflow.com/questions/tagged/tekore>`_.

Installation
============
Tekore can be installed from the Package Index via ``pip``.

.. code:: sh

    $ pip install tekore

Changelog
=========
A detailed changelog can be found on our RTD documentation's
`Release notes <https://tekore.readthedocs.io/page/release_notes.html>`_.

Versioning
==========
When requiring Tekore in projects or other packages,
please pin the version down to at least a specific major release
to avoid compatibility issues.
For example:

.. code:: python

    setup(
        install_requires=[
            'tekore~=4.0'
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


.. |logo| image:: https://raw.githubusercontent.com/felix-hilden/tekore/master/docs/src/logo_small.png
   :alt: logo

.. |python| image:: https://img.shields.io/pypi/pyversions/tekore
   :alt: python version

.. |downloads| image:: https://pepy.tech/badge/tekore/month
   :alt: monthly downloads

.. _github: https://github.com/felix-hilden/tekore
.. _read the docs: https://tekore.readthedocs.io
.. _web api: https://developer.spotify.com/documentation/web-api
