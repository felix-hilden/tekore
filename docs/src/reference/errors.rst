.. _errors:
.. currentmodule:: tekore

Errors
======
Web errors for :ref:`auth` and :ref:`client`.

.. autosummary::
   :nosignatures:

   HTTPError
   BadRequest
   Unauthorised
   Forbidden
   NotFound
   TooManyRequests
   InternalServerError
   BadGateway
   ServiceUnavailable


Clients facing the Web API raise errors when recieving bad status codes.
Specific errors or all web errors can be caught.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    token = tk.request_client_token(*conf[:2])
    spotify = tk.Spotify(token)

    try:
        spotify.album('not-a-real-album')
    except tk.BadRequest:
        print('Whoops, bad request!')
    except tk.HTTPError:
        print('Something is seriously wrong.')

.. autoclass:: HTTPError
.. autoclass:: BadRequest
.. autoclass:: Unauthorised
.. autoclass:: Forbidden
.. autoclass:: NotFound
.. autoclass:: TooManyRequests
.. autoclass:: InternalServerError
.. autoclass:: BadGateway
.. autoclass:: ServiceUnavailable
