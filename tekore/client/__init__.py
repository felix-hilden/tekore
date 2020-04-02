"""
Web API endpoints.

Each method of the client corresponds to an API call, with some exceptions.
Further documentation on endpoints can be viewed in the Web API
`reference <https://developer.spotify.com/documentation/web-api/reference/>`_.

.. code:: python

    from tekore import Spotify

    # Initialise the client
    spotify = Spotify(token)

    # Call the API
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')
    for track in album.tracks.items:
        print(track.track_number, track.name)

Full client
-----------
.. currentmodule:: tekore.client

.. autoclass:: Spotify
   :members:
   :show-inheritance:

   .. automethod:: __init__

Paging navigation
-----------------

.. currentmodule:: tekore.client.paging

.. autoclass:: SpotifyPaging
   :members:

.. currentmodule:: tekore.client.api

Album API
---------
.. autoclass:: SpotifyAlbum
   :members:

Artist API
----------
.. autoclass:: SpotifyArtist
   :members:

Browse API
----------
.. autoclass:: SpotifyBrowse
   :members:

Episode API
-----------
.. autoclass:: SpotifyEpisode
   :members:

Follow API
----------
.. autoclass:: SpotifyFollow
   :members:

Library API
-----------
.. autoclass:: SpotifyLibrary
   :members:

Personalisation API
-------------------
.. autoclass:: SpotifyPersonalisation
   :members:

Player API
----------
.. autoclass:: SpotifyPlayer
   :members:
   :inherited-members:

Playlist API
------------
.. autoclass:: SpotifyPlaylist
   :members:
   :inherited-members:

Search API
----------
.. autoclass:: SpotifySearch
   :members:

Show API
--------
.. autoclass:: SpotifyShow
   :members:


Track API
---------
.. autoclass:: SpotifyTrack
   :members:

User API
--------
.. autoclass:: SpotifyUser
   :members:
"""

from tekore.client.full import Spotify
