'''
     Script Name: webapp.py
     Purpose: ECE 4813 - Cloud Computing Project
     Description: Flask Front-End for Interactive Query Project
     Authors: Shivam Agarwal, Jason Mar, Keary Mobley, Saketh Poda, Carlos Ramirez, Soma Yamaoka
'''

from flask import Flask
import json, requests
import boto

app = Flask(__name__)



'''
Not sure if the below functions are needed. I'm kind of following the templates from these repos
https://github.com/pallets/flask/tree/master/examples/flaskr
https://github.com/pallets/flask/tree/master/examples/minitwit

'''
#def connectdb():
    #Connects to redshift


#def closedb():
    #Close connection to redshift


'''
Here I plan to implement  the api/ queries?
'''


@approute('/')


@approute('/search')
