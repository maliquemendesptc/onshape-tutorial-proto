from flask import Flask, url_for, session
from flask_cors import CORS
from flask_session import Session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object('config')

Session(app)
CORS(app, supports_credentials=True)

oauth = OAuth(app)

oauth.register(name='onshape',
               access_token_url='https://oauth.onshape.com/oauth/token',
               authorize_url='https://oauth.onshape.com/oauth/authorize')


@app.route('/')
def homepage():
  user = session.get('user')
  return render_template('home.html', user=user)


@app.route('/login')
def login():
  redirect_uri = url_for('auth', _scheme="https", _external=True)
  return oauth.onshape.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
  token = oauth.onshape.authorize_access_token()
  resp = oauth.onshape.get('https://cad.onshape.com/api/users/sessioninfo')
  user = resp.json()
  session['user'] = user
  session['token'] = token
  return redirect('/')


@app.route('/logout')
def logout():
  session.pop('user', None)
  session.pop('token', None)
  return redirect('/')


@app.route('/set_session')
def set_session():
  session['test'] = 'foo'
  value = session.get('test')
  print(value)
  return 'set session'


@app.route('/read_session')
def read_session():
  value = session.get('test')
  print(value)
  return "attempted"


# @token_update.connect_via(app)
# def on_token_update(sender,
#                     name,
#                     token,
#                     refresh_token=None,
#                     access_token=None):
#   if refresh_token:
#     item = OAuth2Token.find(name=name, refresh_token=refresh_token)
#   elif access_token:
#     item = OAuth2Token.find(name=name, access_token=access_token)
#   else:
#     return

#   # update old token
#   item.access_token = token['access_token']
#   item.refresh_token = token.get('refresh_token')
#   item.expires_at = token['expires_at']
#   item.save()

app.run(host='0.0.0.0', port=443)
