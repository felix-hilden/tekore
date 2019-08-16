# spotipy
A client for the Spotify Web API.

### plamere/spotipy
Replaces [plamere/spotipy](https://github.com/plamere/spotipy), which has not been maintained since the end of 2017.
Although refactored heavily from its original source, this package does largely rely on the original structure that
was put in place by plamere.

### References
#### Spotify Web API
- [Object model](https://developer.spotify.com/documentation/web-api/reference/object-model/)
- [Authorisation scopes](https://developer.spotify.com/documentation/general/guides/scopes/)

### Design
Some work needs to be done and design decisions have to be made.
Here's a list of items currently under consideration.

- TODO: Fake test-driven development
- TODO: (ReadTheDocs/Sphinx) documentation and tutorials
- TODO: Determine if plural-named fields that are documented as a single object return a list instead
- TODO: Playlist image upload
- How should scope-limited calls and response values be handled? For values perhaps default values or new types.
- Should the library implement client and user token handling and refreshing or just provide the token methods?
- Consider if model bases should be named `Track` and `Album` or `TrackBase` and `AlbumBase`.
Names without `Base` are nice for type hinting, but if they are never used in the same context,
`FullTrack` is a worse name than simply `Track`.
