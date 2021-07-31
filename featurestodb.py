import os
import pymongo
#import adminupload

#db = adminupload.db
db = 'ImageDB'
port= 27018
directory = os.getcwd() + "/photos/annotations"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]


"""
newfile = adminupload.newfile

def getFilePath():
	i = 0
	filepaths = [None] * 50000
	for filename in os.listdir(directory):
		filepaths[i] = directory + "\\" + filename
		i = i + 1
	return filepaths

files = getFilePath()	


"""
"""for x in mydoc:
	fileObject = open(files[i], "r")
	data = fileObject.read()
	myquery = x
	newvalues = { "$set": { "metadata.annotations": data} } 
	mycol.update_one(myquery, newvalues)
	print('updated' + str(i))
	i = i + 1
	"""	

i = 0
for x in os.listdir(directory):	
	fileObject = open(directory + "/" + x, "r")
	data = fileObject.read()
	filename1 = os.path.splitext(directory + "/" + x) [0]
	filename = os.path.basename(filename1)
	print(filename)
	myquery = {"filename": filename}
	newvalues = { "$set": { "metadata.annotations": data} } 
	mycol.update_one(myquery, newvalues)
	print('updated' + str(i))	
	i = i + 1
	fileObject.close()
"""
for x in adminupload.annotations:
	os.remove(directory + '\\' + x)
"""