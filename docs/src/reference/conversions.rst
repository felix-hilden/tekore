.. _conversions:

Conversions
===========
Conversions between Spotify IDs, URIs and URLs.

.. currentmodule:: tekore
.. autosummary::
   :nosignatures:

   to_uri
   to_url
   from_uri
   from_url
   ConversionError
   IdentifierType
   check_id
   check_type

.. code:: python

    import tekore as tk

    # Create ULR for opening an album in the browser
    mountain = '3RBULTZJ97bvVzZLpxcB0j'
    m_url = tk.to_url('album', mountain)

    # Parse input
    type_, id_ = tk.from_url(m_url)
    print(f'Got type `{type_}` with ID `{id_}`')

.. autofunction:: check_id
.. autofunction:: check_type
.. autoclass:: ConversionError
.. autofunction:: from_uri
.. autofunction:: from_url
.. autofunction:: to_uri
.. autofunction:: to_url
.. autoclass:: IdentifierType
   :undoc-members:
