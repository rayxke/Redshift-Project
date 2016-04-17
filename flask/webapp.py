'''
     Script Name: webapp.py
     Purpose: ECE 4813 - Cloud Computing Project
     Description: Flask Front-End for Interactive Query Project
     Authors: Shivam Agarwal, Jason Mar, Keary Mobley, Saketh Poda, Carlos Ramirez, Soma Yamaoka
'''

from flask import Flask, render_template, url_for, jsonify, request
import json
import boto
import psycopg2
app = Flask(__name__)



'''

Not sure if the below functions are needed. I'm kind of following the templates from these repos
https://github.com/pallets/flask/tree/master/examples/flaskr
https://github.com/pallets/flask/tree/master/examples/minitwit

'''
region = 'us-east-1c'
#port = 5439
databasename = "flickrdata"
username = "jasonmar"
password = ""
key_id = ""
secret_id = ""
addr = "myrs.cyaakgdtpknb.us-east-1.redshift.amazonaws.com"

#Connects to redshift
red_conn = boto.connect_redshift(aws_access_key_id=key_id, aws_secret_access_key=secret_id)
pconn = psycopg2.connect("host= '"+addr+"' port='5439' dbname='"+databasename+"' user='"+username+"' password='"+password+"'")


'''select count(*) as modelcount, modelt.modelval as modelval from (select exifmodel.val as modelval, selecttagt.filenum as filenum from (select tagname as tagname, filenum as filenum from tagsbyfile where tagname = 'computer')selecttagt inner join exifmodel on selecttagt.filenum = exifmodel.filenum)modelt group by modelval order by modelcount desc;
'''

#def closedb():
    #Close connection to redshift


def runQuery(tagname):
   #SQL
   my_query = "select count(*) as modelcount, modelt.modelval as modelval from (select exifmodel.val as modelval, selecttagt.filenum as filenum from  (select tagname as tagname, filenum as filenum from tagsbyfile where tagname ="+"\'"+tagname+"\'"+")selecttagt inner join exifmodel on selecttagt.filenum = exifmodel.filenum)modelt group by modelval order by modelcount desc;"
   cur = pconn.cursor()
   cur.execute(my_query)
   mydict = cur.fetchall()
   import pandas as pd
   df = pd.DataFrame(mydict)
   print df
   return df



'''
Here I plan to implement  the api/ queries?
'''
#runQuery()

@app.route('/')
def homepage():
   #connectdb()
   return render_template('index.html')
   


@app.route('/search',methods=['GET'])
def search_data():
  tag = request.args.get('Tag')
  return jsonify(runQuery(tag.lower()))

#Run the app.

if __name__ == '__main__':
   app.run(debug=True)
