Features
========
Spotipy replaces `plamere/spotipy <https://github.com/plamere/spotipy>`_,
which has not been maintained since the end of 2017.
Although refactored heavily from its original source, this package does
rely on the original structure that was put in place by plamere.

The equivalent functionality of the original Spotipy is already implemented.
Some additional features are also provided and being developed.
Below ``X`` indicates a complete feature and ``/`` an incomplete one.

Basic features
--------------
+-------------------------+----------------------+-----------------+
| Spotify Web API feature | felix-hilden/spotipy | plamere/spotipy |
+=========================+======================+=================+
| Authentication          | X                    | X               |
+-------------------------+----------------------+-----------------+
| Endpoints               | X                    | / (*)           |
+-------------------------+----------------------+-----------------+
| Conditional requests    | (**)                 |                 |
+-------------------------+----------------------+-----------------+

(*) Not all endpoints are implemented

(**) While not directly supported,
they are made possible by creating custom ``Sender`` classes.
See documentation on advanced usage for further details.

Additional features
-------------------
+-------------------------+----------------------+-----------------+
| Feature                 | felix-hilden/spotipy | plamere/spotipy |
+=========================+======================+=================+
| Request retries         | X                    | / (*)           |
+-------------------------+----------------------+-----------------+
| Auto-refreshing token   | X                    |                 |
+-------------------------+----------------------+-----------------+
| Model-based API         | X                    |                 |
+-------------------------+----------------------+-----------------+

(*) Retries implemented for GET requests
