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
If successful, another redirection via ``/callback`` back to the main page
will be performed.
You should now see your Spotify user ID and your currently playing track.
The ID is saved to your session cookies and preserved during navigation.
Logging out deletes the cookie and server-stored access token.

.. code:: python

    import tekore as tk

    from flask import Flask, request, redirect, session

    conf = tk.config_from_environment()
    cred = tk.Credentials(*conf)
    spotify = tk.Spotify()

    users = {}


    def app_factory() -> Flask:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'aliens'

        @app.route('/', methods=['GET'])
        def main():
            user = session.get('user', None)
            in_link = '<a href="/login">login</a>'
            out_link = '<a href="/logout">logout</a>'
            page = f'User ID: {user}<br>You can {in_link} or {out_link}'

            if user is not None:
                token = users[user]

                if token.is_expiring:
                    token = cred.refresh(token)
                    users[user] = token

                try:
                    with spotify.token_as(users[user]):
                        song = spotify.playback_currently_playing()

                    page += f'<br>Now playing: {song.item.name}'
                except Exception:
                    page += '<br>Error in retrieving now playing!'

            return page

        @app.route('/login', methods=['GET'])
        def login():
            auth_url = cred.user_authorisation_url(scope=tk.scope.every)
            return redirect(auth_url, 307)

        @app.route('/callback', methods=['GET'])
        def login_callback():
            code = request.args.get('code', None)

            token = cred.request_user_token(code)
            with spotify.token_as(token):
                info = spotify.current_user()

            session['user'] = info.id
            users[info.id] = token

            return redirect('/', 307)

        @app.route('/logout', methods=['GET'])
        def logout():
            uid = session.pop('user', None)
            if uid is not None:
                users.pop(uid, None)
            return redirect('/', 307)

        return app


    if __name__ == '__main__':
        application = app_factory()
        application.run('127.0.0.1', 5000)
