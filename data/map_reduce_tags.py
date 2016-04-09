#Run this on the mergedtags.txt file generated from the merge_script.py file

from mrjob.job import MRJob
fh = open("tagsMP.txt","w+")
count = 0
class MRmyjob(MRJob):

	def mapper(self, _, line):
		global count
		wordlist = line.split(" ")
		count += 1

		for word in wordlist:

			yield word, count

	def reducer(self, key, list_of_values):
		comb = key.encode('utf-8') + "\t" + str(list(list_of_values)).strip("[]") + "\n"
		print comb
		fh.write(comb)

		yield key,list_of_values

if __name__ == '__main__':
    MRmyjob.run()
    fh.close()




