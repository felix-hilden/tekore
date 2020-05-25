.. _senders:

Senders
=======
Manipulate the way clients send requests.

.. currentmodule:: tekore
.. autosummary::
   :nosignatures:

   TransientSender
   AsyncTransientSender
   PersistentSender
   AsyncPersistentSender
   SingletonSender
   AsyncSingletonSender
   RetryingSender
   CachingSender

See also :ref:`senders-bases` and :ref:`senders-options`.

Senders provide a hook between
defining a request and sending it to the Web API.
The sender of a :class:`Client` also determines whether synchronous or
asynchronous calls are used to send requests and process responses.

Sender instances are passed to a client at initialisation.

.. code:: python

    import tekore as tk

    tk.Credentials(*conf, sender=tk.PersistentSender())
    tk.Spotify(sender=tk.AsyncTransientSender())

Synchronous senders wrap around the :mod:`requests` library,
while asynchronous senders use :mod:`httpx`.
Senders accept additional keyword arguments to :meth:`requests.Session.send`
or :meth:`httpx.AsyncClient.request` that are passed on each request.

.. code:: python

    proxies = {
        'http': 'http://10.10.10.10:8000',
        'https': 'http://10.10.10.10:8000',
    }
    tk.TransientSender(proxies=proxies)

Custom instances of :class:`requests.Session` or :class:`httpx.AsyncClient`
can also be used.

.. code:: python

    from requests import Session

    session = Session()
    session.proxies = proxies

    # Attach the session to a sender
    tk.PersistentSender(session)
    tk.SingletonSender.session = session

Concrete senders
----------------
Final senders in a possible chain that concretely make the request to Spotify.

.. autoclass:: TransientSender
.. autoclass:: AsyncTransientSender
.. autoclass:: PersistentSender
.. autoclass:: AsyncPersistentSender
.. autoclass:: SingletonSender
.. autoclass:: AsyncSingletonSender

Extending senders
-----------------
Senders that extend the functionality of other senders.

.. autoclass:: RetryingSender
.. autoclass:: CachingSender

.. _senders-bases:

Sender bases
------------
Bases for subclassing or other endeavours.

.. autosummary::
   :nosignatures:

   Sender
   SyncSender
   AsyncSender
   ExtendingSender
   SenderConflictWarning
   Client

.. autoclass:: Sender
.. autoclass:: SyncSender
.. autoclass:: AsyncSender
.. autoclass:: ExtendingSender
.. autoclass:: SenderConflictWarning
.. autoclass:: Client
   :no-show-inheritance:

.. _senders-options:

Options
-------
Default senders and keyword arguments can be changed.
:attr:`default_sender_instance` has precedence over
:attr:`default_sender_type`.
Using an :class:`ExtendingSender` as the default type will raise an error
as it tries to instantiate itself recursively.
Use :attr:`default_sender_instance` instead.

.. code:: python

    tk.default_sender_type = tk.PersistentSender
    tk.default_sender_instance = tk.RetryingSender()
    tk.default_requests_kwargs = {'proxies': proxies}

    # Now the following are equal
    tk.Spotify()
    tk.Spotify(
        sender=tk.RetryingSender(
            sender=tk.PersistentSender(proxies=proxies)
        )
    )

See also :attr:`default_httpx_kwargs` for asynchronous senders.

.. autodata:: default_requests_kwargs
.. autodata:: default_httpx_kwargs
.. autodata:: default_sender_type
.. autodata:: default_sender_instance
