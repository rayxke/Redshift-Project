'''
Script Name: webapp.py
Purpose: ECE 4813 - Cloud Computing Project
Description: Flask Front-End for Interactive Query Project
Authors: Shivam Agarwal, Jason Mar, Keary Mobley, Saketh Poda, Carlos Ramirez, Soma Yamaoka
'''

from flask import Flask
import json, requests


app = Flask(__name__)
