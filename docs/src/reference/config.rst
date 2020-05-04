.. _config:
.. currentmodule:: tekore

Configuration
=============
Importing and exporting application credentials.

.. autosummary::
   :nosignatures:

   config_from_environment
   config_from_file
   config_to_file
   MissingConfigurationWarning

   client_id_var
   client_secret_var
   redirect_uri_var
   user_refresh_var

Configuration values are read from preset names, which can be changed.
Note that changing values requires importing Tekore as a module.

.. code:: python

    import tekore as tk

    tk.client_id_var = 'your_id_name'
    tk.client_secret_var = 'your_secret_name'
    tk.redirect_uri_var = 'your_uri_name'
    tk.user_refresh_var = 'your_refresh_name'

.. autofunction:: config_from_environment
.. autofunction:: config_from_file
.. autofunction:: config_to_file
.. autoclass:: MissingConfigurationWarning
.. autodata:: client_id_var
.. autodata:: client_secret_var
.. autodata:: redirect_uri_var
.. autodata:: user_refresh_var
