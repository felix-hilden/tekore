.. _senders:

Senders
=======
Manipulate the way clients send requests.

.. currentmodule:: tekore
.. autosummary::
   :nosignatures:

   SyncSender
   AsyncSender
   RetryingSender
   CachingSender

See also :ref:`senders-other`.

Senders provide a hook between
defining a request and sending it to the Web API.
The sender of a :class:`Client` also determines whether synchronous or
asynchronous calls are used to send requests and process responses.

Sender instances are passed to a client at initialisation.

.. code:: python

    import tekore as tk

    tk.Credentials(*conf, sender=tk.SyncSender())
    tk.Spotify(sender=tk.RetryingSender())

Senders wrap around the :mod:`httpx` library
and accept additional keyword arguments to :meth:`httpx.Client`.

.. code:: python

    proxies = {
        'http': 'http://10.10.10.10:8000',
        'https': 'http://10.10.10.10:8000',
    }
    tk.SyncSender(proxies=proxies)

Instances of :class:`httpx.Client` or :class:`httpx.AsyncClient`
can also be passed in for a finer control over sender behaviour.

.. code:: python

    from httpx import Client

    client = Client(proxies=proxies)
    tk.SyncSender(client)

Concrete senders
----------------
Final senders in a possible chain that concretely make the request to Spotify.

.. autoclass:: SyncSender
.. autoclass:: AsyncSender

Extending senders
-----------------
Senders that extend the functionality of other senders.

.. autoclass:: RetryingSender
.. autoclass:: CachingSender

.. _senders-other:

Other classes
-------------
Bases for subclassing or other endeavours.

.. autosummary::
   :nosignatures:

   Sender
   ExtendingSender
   SenderConflictWarning
   Client
   Request
   Response

.. autoclass:: Sender
.. autoclass:: ExtendingSender
.. autoclass:: SenderConflictWarning
.. autoclass:: Client
.. autoclass:: Request
   :no-show-inheritance:
.. autoclass:: Response
   :no-show-inheritance:
