from flask import Flask

app = Flask(__name__)

@app.route('/') # use to provide end point. As soon as the endpoint hit, the following fundtion under the decorater get executed.
def welcome():  # This function will run as soon as we enter into this endpoint.
    return "Hello World"

@app.route('/home')
def home():
    return 'welcome to my home'



from Controller import *