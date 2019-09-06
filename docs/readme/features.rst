Feature comparison and roadmap
==============================
Replaces `plamere/spotipy <https://github.com/plamere/spotipy>`_,
which has not been maintained since the end of 2017.
Although refactored heavily from its original source, this package does
largely rely on the original structure that was put in place by plamere.

The equivalent functionality of the original Spotipy is already implemented.
The Spotify Web API also has features, which will be added to the package.
Some additional features are also provided and being developed.
Below ``X`` indicates a complete feature and ``/`` an incomplete one.

Basic features
--------------
+-------------------------+----------------------+-----------------+
| Spotify Web API feature | felix-hilden/spotipy | plamere/spotipy |
+=========================+======================+=================+
| Authorisation           | X                    | X               |
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
| Responses to objects    | / (**)               |                 |
+-------------------------+----------------------+-----------------+

(*) Retries implemented for GET requests

(**) Response objects are implemented, but not yet returned from calls
