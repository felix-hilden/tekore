======
|logo|
======
|build| |documentation| |coverage|

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
You can also ask a question on
`Stack Overflow <https://stackoverflow.com/questions/tagged/tekore>`_.

.. |logo| image:: docs/src/logo_small.png
   :target: `pypi`_
   :alt: logo

.. |build| image:: https://github.com/felix-hilden/tekore/workflows/build/badge.svg
   :target: https://github.com/felix-hilden/tekore/actions
   :alt: build status

.. |documentation| image:: https://readthedocs.org/projects/tekore/badge/?version=latest
   :target: https://tekore.readthedocs.io/en/latest
   :alt: documentation status

.. |coverage| image:: https://api.codeclimate.com/v1/badges/627ab5f90253b59d4c8f/test_coverage
   :target: https://codeclimate.com/github/felix-hilden/tekore/test_coverage
   :alt: test coverage

.. _pypi: https://pypi.org/project/tekore
.. _read the docs: https://tekore.readthedocs.io
