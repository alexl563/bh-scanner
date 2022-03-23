from flask import Flask, render_template
import pymongo
from pymongo import MongoClient
from datetime import datetime

app=Flask(__name__)
cluster = MongoClient("")
db = cluster['bh-scanner']
collection = db['bh-scanner']

@app.route("/")
def home():
  results = collection.find()
  today = datetime.today()

  return render_template("index.html", front_results = results, day = str(today.day), month = str(today.month), year = str(today.year))

  #return f'{result["name"]} is {"checked in" if result["checked-in"] else "not check-in"}'


if(__name__=="__main__"):
    app.run(debug=True)
