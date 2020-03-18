from flask import Flask
import pymongo
from pymongo import MongoClient
import json
from flask import flash, render_template, request, redirect
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["cloud_ass"]
mycol = mydb["search_books"]

app = Flask(__name__,template_folder="template")
req =" "
multikeys = []
catalogue = []
log=[]
frequency=[]

@app.route("/")
def index():
	return render_template('search_page.html')

@app.route("/search",methods=['POST','GET'])
def search():
	start_time=time.time()
	global req
	req= request.form.get('search')
	count =0
	frequency.append(req)
	data = mycol.find({'author':req})
	newdata = mycol.find({'author':req})
	count= mycol.find({'author':req}).count()
	for words in frequency:
		if req in words:
			count =	count+1
		else:
			count =1
	end_time = time.time()- start_time
	logentry={'Keyword': req, "Time taken" : end_time, "Frequency":	count }
	log.append(logentry)
	with open('Logs.json', 'w') as f:
				json.dump(log, f)


	if(count>0):
		for a in newdata:
			entry={'author': req, 'title':(a["title"])}
			catalogue.append(entry)
			with open('Catalogue.json', 'w') as f:
				json.dump(catalogue, f)
		return render_template('search_page.html',data=data)
	else:
		return "Unsuccessful search"


@app.route("/note",methods=['POST','GET'])
def note():
	count= mycol.find({'author':req}).count()
	if(count>0):
		req_note= request.form.get('note')
		entry = {'author': req , 'Note': req_note}
		multikeys.append(entry)
		with open('Note.json', 'w') as f:
			json.dump(multikeys, f)
		return render_template('search_page.html',entry=entry)
	else:
		return "No author found for the entered name"
	

@app.route("/retrieval", methods=['POST','GET'])
def retrieval():
	with open('Note.json') as infile:
		newdata = json.load(infile)
		return render_template('search_page.html',newdata=newdata)
		
if __name__ == '__main__':
	app.run(debug = True)