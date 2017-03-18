import logging
import subprocess as sb
from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

DURATION_SINGLE=8.0
DURATION_DOUBLE=15.8
HS100_IP='192.168.0.115'

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def grind():
    msg=render_template('how_many')
    return question(msg)

@ask.intent("SingleIntent")
def single():
    msg=render_template('single')
    sb.Popen('python grinder_control.py -t %s -d %f' % (HS100_IP,DURATION_SINGLE),shell=True)
    return statement(msg)
    
@ask.intent("DoubleIntent")
def double():
    msg=render_template('double')
    sb.Popen('python grinder_control.py -t %s -d %f' % (HS100_IP,DURATION_DOUBLE),shell=True)
    return statement(msg)
    

if __name__ == '__main__':

    app.run(debug=True)
