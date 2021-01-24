import os
import pymongo
import adminupload

db = adminupload.db
directory = os.getcwd() + "\\..\\..\\uploaded\\annotations"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]



newfile = adminupload.newfile

def getFilePath():
	i = 0
	filepaths = [None] * 50000
	for filename in os.listdir(directory):
		filepaths[i] = directory + "\\" + filename
		i = i + 1
	return filepaths

files = getFilePath()	

i = 0

for x in newfile:
	fileObject = open(directory + '\\' + adminupload.annotations[i], "r")
	data = fileObject.read()
	myquery = {"id": adminupload.ids[i]}
	newvalues = { "$set": { "metadata.annotations": data} } 
	mycol.update_one(myquery, newvalues)
	i = i + 1
	#print('updated' + str(i))
	fileObject.close()

for x in adminupload.annotations:
	os.remove(directory + '\\' + x)