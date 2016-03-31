#Jason Mar
#Use this to merge all tags into one file
#Run this script in the directory containing folders 0-99


rangestart = 0
rangeend = 10000
mergedfile = open('mergedtags.txt', 'w+')
for folderindex in range(0,100):


	print rangestart
	print rangeend
	for i in range(rangestart,rangeend):

		filename = ""
		filename = str(folderindex) + '/' + str(i)+".txt"

		listoftags = []
		with open(filename) as f:
			tags = f.readlines()

			for tag in tags:
				tagsub = tag[:-2]
				print tagsub
				mergedfile.write(tagsub + ' ')
				
			if(i<999999):
				mergedfile.write('\n')


	
	rangestart +=10000
	rangeend +=10000
mergedfile.close()