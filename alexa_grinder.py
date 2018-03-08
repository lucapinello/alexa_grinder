import logging
import subprocess as sb
from flask import Flask, render_template, Response, request, redirect, url_for

from flask_ask import Ask, statement, question, session

import json

app_settings = json.load(open('app_settings.json'))

DURATION_SINGLE=app_settings['DURATION_SINGLE']
DURATION_DOUBLE=app_settings['DURATION_DOUBLE']
HS100_IP=app_settings['HS100_IP']

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def grind_coffee(quantity):
    if quantity=='single':
        sb.Popen('python grinder_control.py -t %s -d %f' % (HS100_IP,DURATION_SINGLE),shell=True)
    elif quantity=='double':
        sb.Popen('python grinder_control.py -t %s -d %f' % (HS100_IP,DURATION_DOUBLE),shell=True)
    else:
        print 'Quantity unknown'

@ask.launch
def grind():
    msg=render_template('how_many')
    return question(msg)

@ask.intent("SingleIntent")
def single():
    msg=render_template('single')
    #sb.Popen('python grinder_control.py -t %s -d %f' % (HS100_IP,DURATION_SINGLE),shell=True)
    grind_coffee('single')
    return statement(msg)
    
@ask.intent("DoubleIntent")
def double():
    msg=render_template('double')
    grind_coffee('double')
    #sb.Popen('python grinder_control.py -t %s -d %f' % (HS100_IP,DURATION_DOUBLE),shell=True)
    return statement(msg)

@app.route("/settings",methods = ['GET', 'POST'])
def settings():
    global DURATION_SINGLE
    global DURATION_DOUBLE	
    global HS100_IP
    if request.method == 'GET':	
    	return render_template('index.html',
				singleDuration=DURATION_SINGLE,
				doubleDuration=DURATION_DOUBLE,
				HS100_IP=HS100_IP)
    elif request.method == 'POST':
	DURATION_SINGLE=float(request.form['singleDuration'])
	DURATION_DOUBLE=float(request.form['doubleDuration'])
	HS100_IP=request.form['HS100_IP']
	with open('app_settings.json', 'w+') as fp:
    		json.dump({'DURATION_SINGLE':DURATION_SINGLE,
			   'DURATION_DOUBLE':DURATION_DOUBLE,
			   'HS100_IP':HS100_IP}, fp)
	return redirect(url_for('settings'))
    
@app.route('/grind/<quantity>', methods = ['GET', 'POST'])
def iftt_grind(quantity):
    if request.method == 'GET':
        grind_coffee(quantity)
        return  'OK GET! Grinding coffee  %s' % quantity

    else:
    	# POST Error 405 Method Not Allowed
    	print 'METHOD NOT POST'

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0',port=5000)
