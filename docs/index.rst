==============
|spotipy_logo|
==============
|travis| |coverage|

A Python library for the Spotify `Web API`_.

Features
========
The `Web API`_ provides access to a plethora of data on music and users.
Spotipy implements these most integral features completely.

- :ref:`Authentication <module-auth>`: client credentials (application token)
  and authorisation code (user token) flows according to the OAuth2 specification.
- :ref:`API endpoints <module-client>`: access to every resource in the API.
  Responses are parsed into :ref:`model classes <module-model>` with explicit
  attributes to ease examining the contents of a response.

Additional features and various convenience modules are provided too.
Please refer to the documentation of each module for more information.

- :ref:`Request retries <advanced-senders>`
- :ref:`Session persistence <advanced-senders>`
- :ref:`Response caching <advanced-caching>` (possible, though not directly supported)
- :ref:`ID, URI and URL conversions <module-convert>`
- :ref:`Access right scopes <module-scope>`
- :ref:`Response serialisation <module-serialise>`
- :ref:`Response pretty-printing <module-serialise>`
- :ref:`Self-refreshing tokens <module-util>`
- :ref:`Credentials from environment variables <module-util>`
- :ref:`Command line prompt for user autentication <module-util>`


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Introduction

   readme/getting_started
   advanced
   recipes/_recipes

.. toctree::
   :maxdepth: 3
   :hidden:
   :glob:
   :caption: Package Reference

   reference/*


.. |travis| image:: https://travis-ci.org/felix-hilden/spotipy.svg?branch=master
   :target: https://travis-ci.org/felix-hilden/spotipy
   :alt: build status

.. |coverage| image:: https://api.codeclimate.com/v1/badges/6cbb70d77e31c4d3b4c6/test_coverage
   :target: https://codeclimate.com/github/felix-hilden/spotipy/test_coverage
   :alt: test coverage

.. |spotipy_logo| image:: spotipy_logo.png
   :alt: spotipy logo
   :width: 275 px
   :target: `github`_

.. _github: https://github.com/felix-hilden/spotipy
.. _web api: https://developer.spotify.com/documentation/web-api
