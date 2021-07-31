import Orange
import os
# importing images
from orangecontrib.imageanalytics.import_images import ImportImages

import time
#import adminupload
import pymongo
#import featurestodb

#t0= time.clock()
db = 'ImageDB'



import_images = ImportImages()

embeddings1 = []
embeddings2 = []
embeddings3 = []
import_images = ImportImages()

path = os.getcwd() + "/photos"
data, err = import_images(path)	

print(data)

imgnames = [None] * len(data)

image_file_paths = [None] * len(data)

for i in range(len(data)):
	from orangecontrib.imageanalytics.image_embedder import ImageEmbedder
	image_file_paths[i] = path + "/" +  str(data[i,'image'])
	imgnames[i] = os.path.basename(image_file_paths[i])

from orangecontrib.imageanalytics.image_embedder import ImageEmbedder
"""
with ImageEmbedder(model='inception-v3') as emb:
	embeddings1 = emb(image_file_paths)

with ImageEmbedder(model='vgg16') as emb:
	embeddings2 = emb(image_file_paths)
"""
with ImageEmbedder(model='vgg19') as emb:
	embeddings3 = emb(image_file_paths)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]

i = 0
for x in imgnames:
	myquery = {"filename": x}
	"""
	newvalues1 = { "$set": { "metadata.Inception-v3": embeddings1[i]} }
	mycol.update_one(myquery, newvalues1)
	
	newvalues2 = { "$set": { "metadata.vgg16Features": embeddings2[i]} }
	mycol.update_one(myquery, newvalues2)
	
	"""
	newvalues3 = { "$set": { "metadata.vgg19Features": embeddings3[i]} }
	mycol.update_one(myquery, newvalues3)
	
	print('Image ' + str(i) + 'updated')
	i= i + 1

"""
path = os.getcwd() + "/photos" #"I:\\Tomcat\\webapps\\proui\\uploaded"
data, err = import_images(path)    

#print(data)

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

newfile = []

for x in imagefilepaths:
	fn1 = filename1 = os.path.splitext(os.path.basename(x)) [0]
	newfile.append(fn1)
q = {}
myclient = pymongo.MongoClient("mongodb://localhost/")
mydb = myclient[db]
mycol = mydb["fs.files"]


i = 0
for y in newfile:
	myquery = {"filename": y}

	newvalues1 = { "$set": { "metadata.Inception-v3": embeddings1[0]} }
	mycol.update_one(myquery, newvalues1)

	newvalues2 = { "$set": { "metadata.vgg16Features": embeddings2[0]} }
	mycol.update_one(myquery, newvalues2)

	newvalues3 = { "$set": { "metadata.vgg19Features": embeddings3[0]} }
	mycol.update_one(myquery, newvalues3)

	print('Image ' + str(i) + 'inserted')
	i = i + 1


import os, shutil
import glob

#files = glob.glob(path + '/*.png')

#for f in files:
    #os.remove(f)
"""
#t1 = time.clock() - t0
#print("Time elapsed: ", t1)

