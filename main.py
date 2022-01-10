from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime as dt
import os
import ssl
import bson

try:
  import dotenv
  dotenv.load_dotenv('.env')
except ModuleNotFoundError:
  pass

app = Flask(__name__)


client = MongoClient(f"mongodb+srv://root:{os.environ['password']}@hackathon-db.rze2u.mongodb.net/Code?retryWrites=true&w=majority")
db = client.snippets
snippets = db.snippets

@app.route('/')
def index():
  snips = snippets.find()
  return render_template('index.html', title='Home', snippets=snips)

@app.route('/snippet')
def snippet():
  snippet_id = request.args['id']
  snip = snippets.find_one({'_id':bson.ObjectId(snippet_id)})
  return render_template('snippet.html', snippet=snip)

@app.route('/new-snippet')
@app.route('/add')
def add_snippet():
  snip = {
    'title':request.args['title'],
    'short_description':request.args['short_description'],
    'explanation':request.args['explanation'],
    'code':request.args['code'],
    '_time':dt.today()
  }
  snippets.insert_one(snip)
  return redirect(url_for('index'))
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')