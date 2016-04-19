'''
     Script Name: webapp.py
     Purpose: ECE 4813 - Cloud Computing Project
     Description: Flask Front-End for Interactive Query Project
'''

from flask import Flask, render_template, url_for, jsonify, request
import json
import boto
import psycopg2
import pygal
from pygal.style import CleanStyle
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

'''

#Constructs the SQL Query based on the tag, number of results, and fields selected
def constructQuery(tag,numresults,fields,exact):

	'''Example Query
		select count(*) as totalcount, joinedtable.makeval as makeval, joinedtable.modelval as modelval from 
		(select exifmake.val as makeval, exifmodel.val as modelval, selectedtagtable.filenum as filenum from 
		(select tagname as tagname, filenum as filenum from tagsbyfile where tagname ='food')selectedtagtable 
		inner join exifmake on selectedtagtable.filenum = exifmake.filenum 
		inner join exifmodel on selectedtagtable.filenum = exifmodel.filenum )joinedtable 
		group by makeval, modelval order by totalcount desc limit 10;
	'''
	count_section = "select count(*) as totalcount, joinedtable." 
	selectjoin_section = "(" + "select exif"
	innerjoin_section = ""
	group_section = " group by "

	fixedtag = ""
	if exact == None:
		fixedtag = "="+"\'"+tag.lower()+"\'"
	else:
		fixedtag = " LIKE "+"\'" +"%"+tag.lower()+ +"%"+"\'"


	print fixedtag
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
	group_section += "order by totalcount desc limit " + str(numresults) + ";"

	basic_tag_query = "(select tagname as tagname, filenum as filenum from tagsbyfile where tagname" +fixedtag +")selectedtagtable "
	
	query = count_section + selectjoin_section + basic_tag_query + innerjoin_section + group_section

	return query

#gets the checked fields from the html and returns a list of fields checked
def get_checked_fields():

	fieldholder = ['make','model', 'exposure', 'isospeed','aperture','shutterspeed','flash', 'colorspace','compression','contrast','focallength','orientation','saturation','scenecapturetype','sharpness','software','subjectdistancerange','whitebalance']
	tag = request.args.get('tag')
	numresults = request.args.get('numresults')
	checkedholder = []
	for index in range(len(fieldholder)):
		checkedholder.append(request.args.get(fieldholder[index]))

	fieldschecked = []

	for index in range(len(fieldholder)):
		if(checkedholder[index]=='on'):
			fieldschecked.append(fieldholder[index])
	return fieldschecked

#queries for data and restructures the data suitable for JSON
def search_data():

	tag = request.args.get('tag')
	numresults = request.args.get('numresults')
	exact = request.args.get('exact')
	fieldschecked = get_checked_fields()
	constructed_tag = constructQuery(tag,numresults,fieldschecked,exact)
	queryresult = runQuery(constructed_tag)
	print queryresult
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

  	return restructured_result

#runs the query with psycopg2
def runQuery(query):
   #SQL
   cur = pconn.cursor()
   cur.execute(query)
   mylist = cur.fetchall()
   return mylist
   # import pandas as pd
   # df = pd.DataFrame(mydict)
   # df.set_index('0').to_dict()
   # return df


#index page
@app.route('/',methods = ['GET','POST'])
def homepage(result=None):
	if request.args.get('tag',None):
		data = search_data()
		return render_template('index.html',graph15 = draw_bar_graph(data))
	else:
		return render_template('index.html',graph15 = draw_bar_graph(None))

#generates the pygal graph
@app.route('/graph')
def draw_bar_graph(data):

	bar_chart = pygal.Bar(width=900, height=900, explicit_size=True, x_label_rotation=40, style=CleanStyle,truncate_legend=-1,legend_at_bottom=True, legend_at_bottom_columns=1)
	if (data == None):
		bar_chart.title = "Please input fields above"
	else:
		fieldschecked = get_checked_fields()
		bar_chart.title = ", ".join(fieldschecked)
		for index in range(len(data)):
			label = ""
			for labelindex in range(len(data[index][1])):
				label += data[index][1][labelindex] + " "
			bar_chart.add(label,data[index][0])

	html = """%s""" % bar_chart.render()
	return html.decode("utf8")


#Run the app.

if __name__ == '__main__':
   app.run(debug=True)
