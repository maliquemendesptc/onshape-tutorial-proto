from flask import Flask, url_for, session, request
from flask_cors import CORS
from flask_session import Session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
import json
import os

# Creates the Flask app which will have the server configuration and routes
app = Flask(__name__)

# Configures the Flask app to use cookies and authenticate to Onshape
app.config.from_object('config')
Session(app)
CORS(app, supports_credentials=True)
oauth = OAuth(app)
oauth.register(
  name='onshape',
  access_token_url='https://oauth.onshape.com/oauth/token',
  authorize_url='https://oauth.onshape.com/oauth/authorize',
  fetch_token=lambda: session.get(
    'token')  # TODO: DON'T DO IT IN PRODUCTION - but it works?
)


# The base route for the app (https://onshape-tutorial-proto.markcheli.repl.co/)
@app.route('/')
def homepage():
  user = session.get('user')
  doc_id = request.args.get('documentId')
  ele_id = request.args.get('elementId')
  history_type = request.args.get('workspaceOrVersion')
  history_id = request.args.get('workspaceOrVersionId')

  if history_type:
    url = f'https://cad.onshape.com/api/v6/documents/d/{doc_id}/{history_type}/{history_id}/elements?withThumbnails=false'
    resp = oauth.onshape.get(url)
    elements = resp.json()
    if elements:
      print('Elements list retrieved')

  # Example post request, not in use yet
  # url = f'https://cad.onshape.com/api/v6/partstudios/d/{doc_id}/{history_type}/{history_id}'
  # body = json.dumps({'name': 'NEW PS'})
  # headers = {'Content-Type': 'application/json'}
  # resp = oauth.onshape.post(url, data=body, headers=headers)
  # print(resp)

  return render_template('home.html',
                         user=user,
                         doc_id=doc_id,
                         ele_id=ele_id,
                         workspaceOrVersion=history_type,
                         workspaceOrVersionId=history_id,
                         stack=os.environ['STACK'])


# Route for /login which handles the redirect to Onshape
@app.route('/login')
def login():
  redirect_uri = url_for('auth', _scheme="https", _external=True)
  return oauth.onshape.authorize_redirect(redirect_uri)


# Route for /auth which handles the OAuth callback from Onshape
@app.route('/auth')
def auth():
  token = oauth.onshape.authorize_access_token()
  resp = oauth.onshape.get('https://cad.onshape.com/api/users/sessioninfo')
  user = resp.json()
  session['user'] = user
  session['token'] = token
  return redirect('/')


# Route for /logout which handles the logout of the user
@app.route('/logout')
def logout():
  session.pop('user', None)
  session.pop('token', None)
  return redirect('/')


# Route for /validate - will be used from the client
@app.route('/validate')
def validate():
  return "Valid"


# Route to load the part studio .html template
@app.route('/example')
def get_partstudio():
  return render_template('example.html')


@app.route('/instructions')
def instructions_page():
  instruction_title = "Assembling the Peg"
  hint = True
  return render_template('instructions.html',
                         title=instruction_title,
                         hint=hint)


@app.route('/instructions_nohint')
def instructions_page_nohint():
  instruction_title = "Assembling the Peg"
  hint = False
  return render_template('instructions.html',
                         title=instruction_title,
                         hint=hint)


@app.route('/resources')
def resources_page():
  return render_template('resources.html')


@app.route('/start')
def start_page():
  first_question = True
  second_question = False
  return render_template('start.html', first_question=first_question)


@app.route('/next')
def next_question():
  first_question = False
  second_question = True
  return render_template('start.html', second_question=second_question)


# TODO: Update token when expired - maybe?
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

# Runs the app once its been configured
app.run(host='0.0.0.0', debug=True, port=443)
