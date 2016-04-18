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
#region of Redshift Datastore
region = 'us-east-1c'

#Redshift db name
databasename = "flickrdata"

#Redshift master user and password
username = "jasonmar"
password = ""

#AWS Key and Secret
key_id = ""
secret_id = ""

#Redshift endpoint
addr = "myrs.cyaakgdtpknb.us-east-1.redshift.amazonaws.com"

#Connects to redshift
red_conn = boto.connect_redshift(aws_access_key_id=key_id, aws_secret_access_key=secret_id)
pconn = psycopg2.connect("host= '"+addr+"' port='5439' dbname='"+databasename+"' user='"+username+"' password='"+password+"'")


'''
select count(*) as totalcount, joinedtable.makeval as makeval, joinedtable.modelval as modelval from 
(select exifmake.val as makeval, exifmodel.val as modelval, selectedtagtable.filenum as filenum from 
	(select tagname as tagname, filenum as filenum from tagsbyfile where tagname ='food')selectedtagtable 
	inner join exifmake on selectedtagtable.filenum = exifmake.filenum 
	inner join exifmodel on selectedtagtable.filenum = exifmodel.filenum )joinedtable 
group by makeval, modelval order by totalcount desc limit 10;
'''

#def closedb():
    #Close connection to redshift

def constructQuery(tag,fields):

	count_section = "select count(*) as totalcount, joinedtable." 
	selectjoin_section = "(" + "select exif"
	innerjoin_section = ""
	group_section = " group by "

	for index in range(len(fields)):
		count_section += fields[index] + "val" + " as " + fields[index] + "val"
		selectjoin_section += fields[index] + ".val" + " as " + fields[index] + "val"
		innerjoin_section += "inner join exif" + fields[index] + " on selectedtagtable.filenum = exif" + fields[index] + ".filenum "
		group_section += fields[index] + "val"

		if (index == len(fields)-1):
			count_section += " from "
			selectjoin_section += ", selectedtagtable.filenum as filenum from "
			group_section += " "
		else:
			count_section += ", joinedtable."
			selectjoin_section += ", exif"
			group_section += ", "

	innerjoin_section += ")joinedtable"
	group_section += "order by totalcount desc limit 10;"

	basic_tag_query = "(select tagname as tagname, filenum as filenum from tagsbyfile where tagname ="+"\'"+tag.lower()+"\'"+")selectedtagtable "
	
	query = count_section + selectjoin_section + basic_tag_query + innerjoin_section + group_section

	return query

def runQuery(query):
   #SQL
   cur = pconn.cursor()
   cur.execute(query)
   mylist = cur.fetchall()
   # sortdict = sorted(mydict, key=lambda x: x[0],reverse=True)
   return mylist
   # import pandas as pd
   # df = pd.DataFrame(mydict)
   # df.set_index('0').to_dict()
   # return df


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
  tag = request.args.get('tag')
  make = request.args.get('make')
  model = request.args.get('model')

  constructed_tag = constructQuery(tag,['make','model'])
  queryresult = runQuery(constructed_tag)

  #restructure the result so that it is a jsonable structure
  restructured_result = []
  for index in range(len(queryresult)):
  	occurlist = []
  	occurences = int(queryresult[index][0])
  	fieldlist = []
  	for listindex in range(1,len(queryresult[index])):
  		fieldlist.append(queryresult[index][listindex])
  	occurlist.append(occurences)
  	occurlist.append(fieldlist)
  	restructured_result.append(occurlist)
  
  print restructured_result

  return jsonify(restructured_result)

#Run the app.

if __name__ == '__main__':
   app.run(debug=True)
