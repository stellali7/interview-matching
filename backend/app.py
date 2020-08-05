from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.interview_matcher

#def init_database():
#    import json
#    try:
#        from urllib.parse import quote_plus
#    except ImportError:
#        # Python 2.x
#        from urllib import quote_plus

#    with open('mongo.json') as f:
#        config = json.load(f)
#    uri = "mongodb://%s:%s@%s" % (
#        quote_plus(config['user']), quote_plus(config['password']), quote_plus(config['host']))
#    return pymongo.MongoClient(uri)


#client = init_database()
#db = client.meteor
#app = Flask(__name__)
#app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  #session.clear()
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  print(session['user']['role'])
  if session['user']['role'] == "Admin":
    return render_template('dashboard-admin.html')
  elif session['user']['role'] == "Interviewer":
    return render_template('dashboard-interviewer.html')
  else:
    return render_template('dashboard-interviewee.html')

@app.route('/success/')
def success():
  return render_template('success.html')

@app.route('/check-schedule/')
def checkSchedule():
  #session.clear()
  return render_template('check-schedule.html')

@app.route('/schedule/')
@login_required
def schedule():
  print(session['user']['role'])
  if session['user']['role'] == "Admin":
    return render_template('schedule-admin.html')
  elif session['user']['role'] == "Interviewer":
    return render_template('schedule-interviewer.html')
  else:
    return render_template('schedule-interviewee.html')