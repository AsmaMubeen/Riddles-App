from wit import Wit
import requests
from src import app
from flask import Flask, render_template, request, redirect, make_response, abort, jsonify, url_for
import json
import os
from bs4 import BeautifulSoup, SoupStrainer
from os.path import join, dirname
from dotenv import load_dotenv

# from flask import jsonify

#@app.route("/")
#def home():
#   return render_template('index.html')

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")

access_token = os.environ["ACCESS_TOKEN"]

client = Wit(access_token = access_token)

app = Flask(__name__)





@app.route("/", methods = ['GET','POST'])
def index():
	message_text = request.form['input']

	response = client.message(message_text)
	
	riddleTypeList = []
		
	for key, val in response['entities'].items():
		if len(val)>0:
			riddleTypeList.append({'entityType':key,'entityValue': val[0]['value']})
		
	#return json.dumps(riddleTypeList)
	if riddleTypeList[0]['entityType'] == "riddletype":

		if riddleTypeList[0]['entityValue'] == "random" :
			return redirect(url_for('printr'))

		elif riddleTypeList[0]['entityValue'] == "math" :
			return redirect(url_for('printm'))

		elif riddleTypeList[0]['entityValue'] == "logic" :
			return redirect(url_for('printl'))

		elif riddleTypeList[0]['entityValue'] == "whatami" :
			return redirect(url_for('printwai'))

		#elif riddleTypeList[0]['entityValue'] == "hard" :
			#return redirect(url_for('print_hard'))

		elif riddleTypeList[0]['entityValue'] == "funny" :
			return redirect(url_for('print_fun'))
		
		#elif riddleTypeList[0]['entityValue'] == "best" :
			#return redirect(url_for('printb'))

	elif riddleTypeList[0]['entityType'] == "searchType":

		return redirect(url_for('print_search', keyword = riddleTypeList[0]['entityValue']))

@app.route("/search/<keyword>", methods = ['GET','POST'])
def print_search(keyword):
	page_search = requests.get("http://goodriddlesnow.com/riddles/find?name=" + keyword)
	only_tags_with_id = SoupStrainer(id="search-riddles")

	#keyword = riddleTypeList[0]['entityValue']
	#return keyword

	respList = []

	if page_search.status_code == 200:

		soup = BeautifulSoup(page_search.content, 'html.parser', parse_only= only_tags_with_id)
		#return soup.prettify()

		riddle_soup1 = soup.find_all("div", class_ = "riddle panel")
		
		count = 0
		for riddle in riddle_soup1:
			#respList.append({'riddle':riddle.get_text()})
			question_soup = riddle.find("div" , class_ = "riddle-question")#.find("p")
			#question_soup.find("strong").decompose()
			#question_soup.find("br").decompose()
			#question = question_soup.get_text(" ", strip=True)
			question = question_soup.prettify()
			#question = question_soup.get_text()
			#question = question.replace("\n", " ")
			respList.append(question)

			answer_soup = riddle.find("div", class_ = "riddle-answer hide print-show")#.find("p")
			#answer_soup.find("strong").decompose()
			#answer = answer_soup.get_text(" ", strip=True)
			answer_soup.find("hr").decompose()
			answer_soup.find("div", class_ = "riddle-answered-outer print-hide").find("p").find("i").decompose()
			#answer = answer_soup.get_text()
			#answer = answer.replace("\n", " ")
			answer = answer_soup.prettify() 
			count = count + 1
			respList.append(answer)
			#respList.append({'question': question , 'answer': answer})


		#return json.dumps(respList)
		return keyword + respList[0] + respList[1] 
		
		 
	else:
		return page_search.status_code


if __name__ == "__main__":
	app.run()

