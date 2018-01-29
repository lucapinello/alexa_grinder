import logging
import subprocess as sb
from flask import Flask, render_template, request

from flask_ask import Ask, statement, question, session

DURATION_SINGLE=8.3
DURATION_DOUBLE=15.4
HS100_IP='192.168.0.115'

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
