# alexa_grinder

Voice controlled grinder with precise timing using TP-link HS100 and Amazon alexa.

Based on flask-ask (https://github.com/johnwheeler/flask-ask) and (https://github.com/softScheck/tplink-smartplug) 

To run with you Alexa:

Open the file alexa_grinder.py and change the settings:

DURATION_SINGLE=8.0  #grinding time for a single cup
DURATION_DOUBLE=15.6 #grinding time for a single cup
HS100_IP='192.168.0.115' #ip of the tp-link hs100 smart plug

Run

python alexa_grinder.py

You need also to install ngrok (https://ngrok.com/)

Run 

ngrok http 5000

Create an alexa skill at: https://developer.amazon.com/edw/home.html

Use the intentes and the utterances provided.

Enjoy!
