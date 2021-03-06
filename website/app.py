from flask import Flask
import datetime
import time
from flask import *
from config import *
import requests
import pygal
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/')
def dashboard(methods=['GET', 'POST', 'PUT']):
    uri = "https://sidhy-33818.firebaseio.com/.json"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    confidence = data['confidence']  # <-- The display name
    question = data['question']  # <-- The reputation

    votes = data['votes']

    bar_chart = pygal.Bar(width=600, height=600,
                          explicit_size=True, title="Confidence")

    pie_char = pygal.Pie()

    pie_char.title = "Quiz Result"

    for x in votes.keys():
        pie_char.add(x, votes[x])
    imp_temps = list(confidence.values())

    total_temp_votes_on_confidence = 0
    for x in imp_temps:
        total_temp_votes_on_confidence += int(x)
    if total_temp_votes_on_confidence != 0:
        for x in range(len(imp_temps)):
            imp_temps[x] = imp_temps[x]/total_temp_votes_on_confidence*100

    bar_chart.x_labels = sorted(list(confidence.keys()))
    bar_chart.add('Confidence', imp_temps)
    return render_template("index.html", bar_chart=bar_chart, questions=enumerate(question), pie_chart=pie_char)


@app.route('/delete/<int:qid>')
def delete_post(qid):
    uri = "https://sidhy-33818.firebaseio.com/.json"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    confidence = data['confidence']  # <-- The display name
    question = data['question']  # <-- The reputation

    votes = data['votes']

    question[qid] = '0'
    print(data)
    r = requests.put("https://sidhy-33818.firebaseio.com/.json",
                     data=json.dumps(data))
    print(r.text)
    return redirect('/')
