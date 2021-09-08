.. _auth-server:

Authenticating server
=====================
The scripts below detail how to start up a simple authentication sever.

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

    The :code:`auths` dictionary could be used to store arbitrary information.
    In this example it is used to map the state parameters
    of ongoing authorisations to :class:`UserAuth <tekore.UserAuth>` objects.

.. tabs::

   .. tab:: Flask

      .. code:: python

          import tekore as tk

          from flask import Flask, request, redirect, session

          conf = tk.config_from_environment()
          cred = tk.Credentials(*conf)
          spotify = tk.Spotify()

          auths = {}  # Ongoing authorisations: state -> UserAuth
          users = {}  # User tokens: state -> token (use state as a user ID)

          in_link = '<a href="/login">login</a>'
          out_link = '<a href="/logout">logout</a>'
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
                      with spotify.token_as(token):
                          playback = spotify.playback_currently_playing()

                      item = playback.item.name if playback else None
                      page += f'<br>Now playing: {item}'
                  except tk.HTTPError:
                      page += '<br>Error in retrieving now playing!'

                  return page

              @app.route('/login', methods=['GET'])
              def login():
                  if 'user' in session:
                      return redirect('/', 307)

                  scope = tk.scope.user_read_currently_playing
                  auth = tk.UserAuth(cred, scope)
                  auths[auth.state] = auth
                  return redirect(auth.url, 307)

              @app.route('/callback', methods=['GET'])
              def login_callback():
                  code = request.args.get('code', None)
                  state = request.args.get('state', None)
                  auth = auths.pop(state, None)

                  if auth is None:
                      return 'Invalid state!', 400

                  token = auth.request_token(code, state)
                  session['user'] = state
                  users[state] = token
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

   .. tab:: FastAPI

      .. code:: python

          import uvicorn
          import tekore as tk
          from fastapi import FastAPI, Request
          from fastapi.responses import RedirectResponse, HTMLResponse
          from starlette.middleware.sessions import SessionMiddleware

          app = FastAPI()
          app.add_middleware(SessionMiddleware, secret_key="secret_key_placeholder")

          conf = tk.config_from_environment()
          cred = tk.Credentials(*conf)
          spotify = tk.Spotify()

          auths = {}  # Ongoing authorisations: state -> UserAuth
          users = {}  # User tokens: state -> token (use state as a user ID)

          in_link = '<a href="/login">login</a>'
          out_link = '<a href="/logout">logout</a>'
          login_msg = f"You can {in_link} or {out_link}"


          @app.get("/", response_class=HTMLResponse)
          def read_root(request: Request):
              user = request.session.get("user", None)
              token = users.get(user, None)

              # Return early if no login or old session
              if user is None or token is None:
                  request.session.pop("user", None)
                  return f"User ID: None<br>{login_msg}"

              page = f"User ID: {user}<br>{login_msg}"
              if token.is_expiring:
                  token = cred.refresh(token)
                  users[user] = token

              try:
                  with spotify.token_as(token):
                      playback = spotify.playback_currently_playing()

                  item = playback.item.name if playback else None
                  page += f"<br>Now playing: {item}"
              except tk.HTTPError:
                  page += "<br>Error in retrieving now playing!"

              return HTMLResponse(content=page, status_code=200)


          @app.get("/login")
          def login(request: Request):
              if "user" in request.session:
                  return RedirectResponse(url="/")

              scope = tk.scope.user_read_currently_playing
              auth = tk.UserAuth(cred, scope)
              auths[auth.state] = auth
              return RedirectResponse(auth.url)


          @app.get("/callback")
          def login_callback(request: Request, code: str, state: str):
              auth = auths.pop(state, None)

              if auth is None:
                  return "Invalid state!", 400

              token = auth.request_token(code, state)
              request.session["user"] = state
              users[state] = token
              return RedirectResponse("/")


          @app.get("/logout")
          def logout(request: Request):
              uid = request.session.pop("user", None)
              if uid is not None:
                  users.pop(uid, None)
              return RedirectResponse("/")


          if __name__ == "__main__":
              uvicorn.run(
                  "main:app",
                  port=5000,
                  host="0.0.0.0",
                  reload=True,
              )
