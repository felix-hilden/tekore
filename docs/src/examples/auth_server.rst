.. _auth-server:

Authenticating server
=====================
The script below starts up a simple Flask web server for authentication.

In this example the configured redirect URI must match
``http://localhost:5000/callback`` and be whitelisted in your
`application <https://developer.spotify.com/dashboard>`_ settings.
Note that the server need not be accessible from the web.
With a server that is hosted elsewhere
or one that needs to be accessible from outside,
whitelist another redirect URI that matches the server's address.

Run the script and navigate to ``localhost:5000`` to see your user ID.
It should be ``None`` before logging in.
During login you will be redirected to authenticate at Spotify.
If access is granted and the state security check passes,
another redirection via ``/callback`` to an info page will be performed.
It should read "successful" and refer you back to the main page.
You should now see a generated user ID and your currently playing track.
The ID is saved to your session cookies and preserved during navigation.
Logging out deletes the cookie and server-stored access token.

.. note::

    The :code:`auths` dictionary can be used to store arbitrary information.
    In this example it is used to map the state parameters
    of ongoing authorisations to redirect destinations.

.. code:: python

    import tekore as tk

    from flask import Flask, request, redirect, session

    conf = tk.config_from_environment()
    cred = tk.Credentials(*conf)
    spotify = tk.Spotify()

    auths = {}  # Ongoing authorisations: state -> redirect destination
    users = {}  # User tokens: state -> token (use state as a user ID)

    in_link = '<a href="/login?redirect=/successful">login</a>'
    out_link = '<a href="/logout?redirect=/successful">logout</a>'
    login_msg = f'You can {in_link} or {out_link}'


    def app_factory() -> Flask:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'aliens'

        @app.route('/', methods=['GET'])
        def main():
            user = session.get('user', None)
            token = users.get(user, None)

            # Return early if no login or old session
            if user is None or token is None:
                session.pop('user', None)
                return f'User ID: None<br>{login_msg}'

            page = f'User ID: {user}<br>{login_msg}'
            if token.is_expiring:
                token = cred.refresh(token)
                users[user] = token

            try:
                with spotify.token_as(users[user]):
                    playback = spotify.playback_currently_playing()

                item = playback.item.name if playback else None
                page += f'<br>Now playing: {item}'
            except tk.HTTPError:
                page += '<br>Error in retrieving now playing!'

            return page

        @app.route('/login', methods=['GET'])
        def login():
            destination = request.args.get('redirect', '/')
            if 'user' in session:
                return redirect(destination, 307)

            state = tk.gen_state()
            scope = tk.scope.user_read_currently_playing
            url = cred.user_authorisation_url(scope, state, show_dialog=True)

            auths[state] = destination
            return redirect(url, 307)

        @app.route('/callback', methods=['GET'])
        def login_callback():
            code = request.args.get('code', None)
            state = request.args.get('state', None)
            destination = auths.pop(state, None)

            if destination is None:
                return 'Invalid state!', 400

            token = cred.request_user_token(code)

            session['user'] = state
            users[state] = token

            return redirect(destination, 307)

        @app.route('/logout', methods=['GET'])
        def logout():
            uid = session.pop('user', None)
            if uid is not None:
                users.pop(uid, None)
            destination = request.args.get('redirect', '/')
            return redirect(destination, 307)

        @app.route('/successful', methods=['GET'])
        def successful():
            return 'Successful! <a href="/">Go home</a>'

        return app


    if __name__ == '__main__':
        application = app_factory()
        application.run('127.0.0.1', 5000)
