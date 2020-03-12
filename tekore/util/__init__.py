"""
Utility module for your convenience <3

.. currentmodule:: tekore.util.config
.. autosummary::
   :nosignatures:

   config_from_environment
   config_from_file
   config_to_file

.. currentmodule:: tekore.util.credentials
.. autosummary::
   :nosignatures:

   request_client_token
   prompt_for_user_token
   refresh_user_token
   parse_code_from_url

The main motivation for this module is to make authorisation effortless.
That goal is achieved by reading and writing configuration,
and functions for easily retrieving access tokens.

Some applications might have different needs,
so please do create your own versions of these routines.
Particularly,
:func:`prompt_for_user_token <tekore.util.credentials.prompt_for_user_token>`
opens up a web browser for the user to log in with,
doesn't expose all parameters that are available
when using lower-level functions, and forces the login dialog to be shown.

Almost everything defined in submodules is imported to
:mod:`util <tekore.util>` for easy access.

config
------
.. automodule:: tekore.util.config
   :members:
   :undoc-members:

credentials
-----------
.. automodule:: tekore.util.credentials
   :members:
   :undoc-members:
"""

from tekore.util.config import (
    config_from_environment,
    config_from_file,
    config_to_file,
)
from tekore.util.credentials import (
    parse_code_from_url,
    prompt_for_user_token,
    refresh_user_token,
    request_client_token,
)
