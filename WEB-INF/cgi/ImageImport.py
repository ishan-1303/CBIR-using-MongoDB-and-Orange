import Orange
import os
from orangecontrib.imageanalytics.import_images import ImportImages

import pymongo
import featurestodb

db = featurestodb.db
port = featurestodb.port

import_images = ImportImages()

#three embedding (features) arrays
embeddings1 = []	#Inception-v3 features
embeddings2 = []	#vgg16Features
embeddings3 = []	#vgg19Features


# importing images
import_images = ImportImages()
path = os.getcwd() + "/../../uploaded"
data, err = import_images(path)    

# defining image path to pass to embedding
print(len(data))
image_file_paths = [None] * len(data)
for i in range(len(data)):
    image_file_paths[i] = path + "/" +  str(data[i,'image'])

# extracting features from images (embedding)
from orangecontrib.imageanalytics.image_embedder import ImageEmbedder
with ImageEmbedder(model='inception-v3') as emb:
	embeddings1 = emb(image_file_paths)

with ImageEmbedder(model='vgg16') as emb:
	embeddings2 = emb(image_file_paths)

with ImageEmbedder(model='vgg19') as emb:
	embeddings3 = emb(image_file_paths)



q = {}
myclient = pymongo.MongoClient("mongodb://localhost/")
mydb = myclient[db]
mycol = mydb["fs.files"]


i = 0
#retrieving embeddings from database
for y in featurestodb.newfile:
	myquery = {"filename": y}

	newvalues1 = { "$set": { "metadata.Inception-v3": embeddings1[0]} }
	mycol.update_one(myquery, newvalues1)

	newvalues2 = { "$set": { "metadata.vgg16Features": embeddings2[0]} }
	mycol.update_one(myquery, newvalues2)

	newvalues3 = { "$set": { "metadata.vgg19Features": embeddings3[0]} }
	mycol.update_one(myquery, newvalues3)

	print('<br>Image ' + str(i) + 'inserted<br>')
	i = i + 1


import os, shutil
import glob

#removing uploaded image and annotation file
files = glob.glob(path + '/*.png')

for f in files:
    os.remove(f)


files = glob.glob(path + 'annotations/*.txt')
for f in files:
    os.remove(f)
    
print('<br><a href="../Admin Login/seite1.html"> Add more images </a>')
