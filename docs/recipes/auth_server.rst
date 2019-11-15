.. _auth-server:

Authenticating server
=====================

The script below starts up a simple Flask web server for authentication.

The configured redirect URI must match ``http://localhost:5000/callback``
and be whitelisted in your
`application <https://developer.spotify.com/dashboard>`_ settings.
Note that the server need not be accessible from the web.

Run the script and navigate to ``localhost:5000`` to see your user ID.
It should be ``None`` before logging in.
During login you will be redirected to authenticate at Spotify.
If successful, another redirection via ``/callback`` back to the main page
will be performed.
You should now see your Spotify user ID.
It is saved to your session cookies and preserved during navigation.
Logging out deletes the cookie and server-stored user information.

.. code:: python

    from flask import Flask, request, redirect, session

    from spotipy import Spotify, Credentials
    from spotipy.util import credentials_from_environment
    from spotipy.scope import every

    conf = credentials_from_environment()
    cred = Credentials(*conf)
    spotify = Spotify()

    users = {}


    def app_factory() -> Flask:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'aliens'

        @app.route('/', methods=['GET'])
        def main():
            in_link = '<a href="/login">login</a>'
            out_link = '<a href="/logout">logout</a>'
            user = session.get('user', None)
            return f'User ID: {user}<br>You can {in_link} or {out_link}'

        @app.route('/login', methods=['GET'])
        def login():
            auth_url = cred.user_authorisation_url(scope=every)
            return redirect(auth_url, 307)

        @app.route('/callback', methods=['GET'])
        def login_callback():
            code = request.args.get('code', None)

            token = cred.request_user_token(code, scope=every)
            with spotify.token_as(token):
                info = spotify.current_user()

            session['user'] = info.id
            users[info.id] = info

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
