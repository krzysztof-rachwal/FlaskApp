import sys 
sys.path.append('Lib')
sys.path.append('/C/Users/krzys/AppData/Local/Programs/Python/Python38-32/Scripts')
from flask import Flask, render_template, request, url_for, jsonify
import numpy as np
from joblib import dump, load
import pickle
import json
#get news url
import requests
from bs4 import BeautifulSoup
#mongodb
from pymongo import MongoClient
import password

# PASSOWRD FILE NOT INCLUDED IN THE PROJECT FILES.

# start a mongodb client
client = MongoClient(f'mongodb://c1968648:{password.PASSWORD}@csmongo.cs.cf.ac.uk:27017/c1968648',ssl=True)

# create an object of our database
db = client.c1968648

### REMEMBER THE CATEGORY MAP ###
#{'chemistry': 0, 'economics': 1, 'literature': 2, 'peace': 3, 'physics': 4, 'medicine': 5}

cmap = dict([(b,a) for a,b in {'Atheism': 0, 'Computer graphics': 1, 'Computers - MS Windows': 2, 'Computer systems, IBM hardware': 3, 'Computers - Mac hardware': 4, 
								'Computers - Windows 10': 5, 'Forsale': 6, 'Autos': 7, 'Motorcycles': 8, 'Sport - Baseball': 9, 'Sport - Hockey': 10,
								'Science - Cryptography': 11, 'Science - Electronics': 12, 'Science - Medicine': 13, 'Scinece - Space': 14, 
								'Sociology Religion Christian': 15, 'Politics Guns': 16, 'Politics Mid-East': 17, 'Politics Mixed': 18, 'Religion Mixed': 19}.items()])

app = Flask(__name__)

@app.route('/')
def form():
	return render_template('index.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
	vectorizer = load('models/vectorizer.joblib')
	#vectorizer = pickle.load(open('models/tfidf_vectorizer.vec', 'rb'))
	print('vectorizer loaded')	
	model = load('models/model.joblib')
	#model = pickle.load(open('models/tfidf_lr.model', 'rb'))
	print('model loaded')
	#get the url of the BBC news article and convert it into text
	user_url=request.form['input_text']
	res = requests.get(user_url)
	soup = BeautifulSoup(res.text, 'html.parser')
	url_text = soup.find('div', { "class" : "story-body__inner" }).text #the story-board__inner class is the div in which the article content is placed on the BBC webpage  
	text=request.form[url_text]
	vec=vectorizer.transform([text])
	pred=model.predict(vec)[0]
	pred=cmap[pred]
	print('prediction: ',pred)
	return render_template(
	'predicted_form.html',
	sentence=text,
	prediction=pred)

@app.route('/feedback_received', methods=['POST'])
def feedback_received():
	print('request: ',list(request.form.keys()))
	feedback = request.form['feedback']	
	sentence = request.form['sentence']
	prediction = request.form['prediction']
	print('prediction: ', prediction)
	print('feedback: ',feedback)
	print('sentence: ',sentence)
	docs = [
		{'category':prediction,
		'value':sentence}
	]
	if feedback == 'correct':
		for d in docs:
			db.predictions.insert_one(d)
		return render_template('feedback_received.html', sentence=sentence, feedback=feedback, prediction=prediction)
	else:
		return render_template('incorrect.html', sentence=sentence)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
