from flask import Flask, url_for, session, request
from flask_cors import CORS
from flask_session import Session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
import os
from instructions import instructions_list

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

@app.route('/instructions/<int:step>')
def instructions_page(step):
  index = step - 1
  instruction_step = instructions_list[index]['instruction_step']
  instruction_title = instructions_list[index]['instruction_title']
  meter_num = step
  instructions = instructions_list[index]['instructions']
  hint_txt = instructions_list[index]['hint_txt']
  imgorvid = instructions_list[index]['imgorvid']
  page_number = str(step) + "/" + str(len(instructions_list))
  # To reference the total number of steps use len(instruction_list)
  prev_button = True
  next_button = True
  next_num = step + 1
  prev_num = step - 1
  hint = True
  if step <= 1:
    prev_button = False
  if step >= len(instructions_list):
    next_button = False

  return render_template('instructions.html',
                         title=instruction_title,
                         hint=hint,
                         step=instruction_step,
                         meter=meter_num,
                         instruction=instructions,
                         hints=hint_txt,
                         img=imgorvid,
                         page=page_number,
                         next_num=next_num,
                         prev_num=prev_num,
                         prev_button=prev_button,
                         next_button=next_button)


@app.route('/instructions_nohint/<int:step>')
def instructions_page_nohint(step):
  index = step - 1
  instruction_step = instructions_list[index]['instruction_step']
  instruction_title = instructions_list[index]['instruction_title']
  meter_num = step
  instructions = instructions_list[index]['instructions']
  hint_txt = instructions_list[index]['hint_txt']
  imgorvid = instructions_list[index]['imgorvid']
  page_number = str(step) + "/" + str(len(instructions_list))
  next_num = step + 1
  prev_num = step - 1
  prev_button = True
  next_button = True
  hint = False
  if step <= 1:
    prev_button = False
  if step >= len(instructions_list):
    next_button = False
  return render_template('instructions.html',
                         title=instruction_title,
                         hint=hint,
                         step=instruction_step,
                         meter=meter_num,
                         instruction=instructions,
                         hints=hint_txt,
                         img=imgorvid,
                         page=page_number,
                         next_num=next_num,
                         prev_num=prev_num,
                         prev_button=prev_button,
                         next_button=next_button)


@app.route('/resources')
def resources_page():
  return render_template('resources.html')

@app.route('/')
def start_page():
  first_question = True
  second_question = False
  return render_template('start.html', first_question=first_question)

@app.route('/next')
def next_question():
  first_question = False
  second_question = True
  return render_template('start.html', second_question=second_question)

# Runs the app once its been configured
app.run(host='0.0.0.0', debug=True, port=443)
