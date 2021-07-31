import pymongo
import cgi
import os
		
myclient = pymongo.MongoClient("mongodb://localhost/")

#to retrieve annotations for particular image in database
def getDescription(db, filename):
	mydb = myclient[db]
	mycol = mydb["fs.files"]
	myDesc = mycol.find_one({"filename":filename}, {"metadata.annotations": 1, "_id":0}) 
	return myDesc

#print(getDescription('ImageDB','ADE_val_00001275.png'))