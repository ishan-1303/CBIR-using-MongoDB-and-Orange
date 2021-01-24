
import pymongo
from upload import db
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]

i = 0
embeddings = []
image_file_paths = []
mydoc = mycol.find({},{"metadata.annotations": 0 })

for x in mydoc:
	embeddings.append(x["metadata"])
	image_file_paths.append(x["filename"])
#print(x["filename"])





#print(embeddings)