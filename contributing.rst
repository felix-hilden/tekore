Contributing
============
|issues_open| |issue_resolution|

Thank you for considering contributing to Tekore!
If you've found a bug or would like to propose a feature,
please submit an `issue <https://github.com/felix-hilden/tekore/issues>`_.

If you'd like to get more involved,
`here's how <https://opensource.guide/how-to-contribute/>`_.
There are many valuable contributions in addition to contributing code!
If you're so inclined, triaging issues, improving documentation,
helping other users and reviewing existing code and PRs is equally appreciated!

The rest of this guide focuses on development and code contributions.

Installation
------------
Start by cloning the most recent version, either from the main repository
or a fork you created, and installing the source as an editable package.
Using a virtual environment of your choice for the installation is recommended.

.. code:: sh

    $ git clone https://github.com/felix-hilden/tekore.git
    $ cd tekore
    $ pip install -e .
    $ pip install -r requirements/dev

The last command installs all the necessary dependencies for development.

If you forked, consider adding the upstream repository as a remote to easily
update your main branch with the latest upstream changes.
For tips and tricks on contributing, see `how to submit a contribution
<https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution>`_,
specifically `opening a pull request
<https://opensource.guide/how-to-contribute/#opening-a-pull-request>`_.

Testing
-------
The installation can be verified, and any changes tested by running tox.

.. code:: sh

    $ tox

Now tests have been run along with other checks and a documentation build.
Tests against the live Web API use environment variables for credentials.
These tests manipulate your data and player,
but try to restore previous state insofar as it is possible.
Please refer to the description of each test class for details.
In order to run all tests successfully, one must specify:

* ``SPOTIFY_CLIENT_ID`` - client ID of a registered Spotify 3rd party application
* ``SPOTIFY_CLIENT_SECRET`` - secret associated with that application
* ``SPOTIFY_REDIRECT_URI`` - redirect URI whitelisted in application settings
* ``SPOTIFY_USER_REFRESH`` - user refresh token with all scopes

In addition, playback tests require an active Spotify device
that does not have a private session enabled and an empty song queue.

Optionally ``TEKORE_TEST_SKIP_IS_FAIL`` can be set to raise an error if some
of the tests would be skipped because of the environment has not been configured.

Developing
----------
A number of tools are used to automate development tasks.
They are available through tox labels.

.. code:: sh

    $ coverage run && coverage report  # execute test suite
    $ tox -m docs  # build documentation to docs/build/html/index.html
    $ tox -m lint  # check code style
    $ tox -m format  # autoformat code
    $ tox -m build  # packaging dry run

Releasing
---------
Before releasing, make sure the version number is incremented
and the release notes reference the new release.
Running tests once more is also good practice.
Tox is used to build the appropriate distributions and publish them on PyPI.
The publish script also reads credentials from a .pypirc file,
so please set that up before publishing.

.. code:: sh

    $ tox -m publish

If you'd like to test the upload and the resulting package,
upload manually to `TestPyPI <https://test.pypi.org>`_ instead.

.. code:: sh

    $ python -m build
    $ twine upload --repository testpypi dist/*
    $ pip install --index-url https://test.pypi.org/simple/ sphinx-codeautolink

.. |issue_resolution| image:: http://isitmaintained.com/badge/resolution/felix-hilden/tekore.svg
   :target: https://isitmaintained.com/project/felix-hilden/tekore
   :alt: issue resolution time

.. |issues_open| image:: http://isitmaintained.com/badge/open/felix-hilden/tekore.svg
   :target: https://isitmaintained.com/project/felix-hilden/tekore
   :alt: open issues

.. _pypi: https://pypi.org/project/tekore
.. _web api: https://developer.spotify.com/documentation/web-api
.. _read the docs: https://tekore.readthedocs.io
