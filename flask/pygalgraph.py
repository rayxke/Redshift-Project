#sudo install pip pygal
#this is just Documentation for the code, it will be modified once we figure out how to fetch data as an array

import pygal
data_val = [1, 2, 3, 4]  #put data values in array format
camera1 = 'Nixon' #additional info such as Camera in a string
bar_chart = pygal.Bar()       #create bar graph
bar_chart.title = "Flickr Queries"    #create title
bar_chart.x_labels = map(str, range(2000,2004))   #x lables
bar_chart.add(camera1, data_val)               #add graph
bar_chart.render_to_file('bar_chart.svg')       #render graph open in browser 
