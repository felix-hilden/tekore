.. _errors:
.. currentmodule:: tekore

Errors
======
Web errors for :ref:`auth` and :ref:`client`.

.. autosummary::
   :nosignatures:

   HTTPError
   ClientError
   ServerError
   BadRequest
   Unauthorised
   Forbidden
   NotFound
   TooManyRequests
   InternalServerError
   BadGateway
   ServiceUnavailable


Clients facing the Web API raise errors when recieving bad status codes.
Only errors documented in the Web API documentation are expected and provided.
Other exceptions are raised as :class:`ClientError` or :class:`ServerError`.

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

Error objects also contain the relevant :class:`Request` and :class:`Response`
objects for closer inspection.

.. code:: python

    try:
        spotify.album('not-a-real-album')
    except tk.BadRequest as ex:
        print(str(ex))
        print(ex.request)
        print(ex.response)

.. autoclass:: HTTPError
.. autoclass:: ClientError
.. autoclass:: ServerError
.. autoclass:: BadRequest
.. autoclass:: Unauthorised
   :undoc-members:
.. autoclass:: Forbidden
.. autoclass:: NotFound
.. autoclass:: TooManyRequests
.. autoclass:: InternalServerError
.. autoclass:: BadGateway
.. autoclass:: ServiceUnavailable
