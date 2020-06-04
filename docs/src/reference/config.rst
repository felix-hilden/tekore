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

Environment variables and configuration files can be used
to provide application and user credentials.
See also :ref:`config-options`.

.. autofunction:: config_from_environment
.. autofunction:: config_from_file
.. autofunction:: config_to_file
.. autoclass:: MissingConfigurationWarning

.. _config-options:

Options
-------
Configuration values are read from and written to preset names.
Those names can be changed to your liking.

.. code:: python

    import tekore as tk

    tk.client_id_var = 'your_client_id_var'
    tk.client_secret_var = 'your_client_secret_var'
    tk.redirect_uri_var = 'your_redirect_uri_var'
    tk.user_refresh_var = 'your_user_refresh_var'

.. note:: Changing values requires importing Tekore as a module as above.

.. autodata:: client_id_var
.. autodata:: client_secret_var
.. autodata:: redirect_uri_var
.. autodata:: user_refresh_var
