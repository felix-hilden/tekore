==============
|spotipy_logo|
==============
|python| |downloads|

Welcome to the Python Package Index page of Spotipy,
a client of the Spotify Web API for Python!
Spotipy allows you to interact with the Web API effortlessly.

.. code:: python

    from spotipy import Spotify

    s = Spotify(token)

    tracks = s.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    s.playback_start_tracks([finlandia])

See our online documentation on `Read The Docs`_ for tutorials,
examples, package reference and a detailed description of features.
Visit our repository on `GitHub`_  if you'd like to submit an issue
or ask just about anything related to Spotipy.

Installation
============
Spotipy can be installed from the Package Index via ``pip``.

.. code:: sh

    $ pip install spotipy

History
=======
Spotipy was originally created by Paul Lamere (plamere) in 2014,
but was abandoned in late 2017.
In an attempt to catch up with the evolving Web API,
Spotipy was rewritten in 2019 and the package ownership transferred.

The latest version published by plamere was numbered 2.4.4.
The latest repository contents were published in version 2.4.5,
which was followed by a functionally identical version 2.5
with warnings of the rewrite that was taking place.
Spotipy 3.0 was the first one to feature the rewritten package.

Documentation of the old package was hosted on Read The Docs too.
That documentation was transferred along with the PyPI name.
It can be found under a different version number `here <rtd old_>`_.

.. |spotipy_logo| image:: docs/spotipy_logo_small.png
   :target: `pypi`_
   :alt: spotipy logo

.. |python| image:: https://img.shields.io/pypi/pyversions/spotipy
   :target: `pypi`_
   :alt: python version

.. |downloads| image:: https://img.shields.io/pypi/dm/spotipy
   :target: https://pypistats.org/packages/spotipy
   :alt: monthly downloads

.. _pypi: https://github.com/felix-hilden/spotipy
.. _github: https://github.com/felix-hilden/spotipy
.. _rtd old: https://spotipy.readthedocs.io
.. _read the docs: https://updated-spotipy-test.readthedocs.io
