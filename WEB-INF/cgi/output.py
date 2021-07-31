import Orange
import pymongo
import os
import upload
from orangecontrib.imageanalytics.import_images import ImportImages
import description
import re
from timeit import default_timer as timer


start = timer()
port = upload.port
myclient = pymongo.MongoClient("mongodb://localhost/")
mydb = myclient[upload.db]
mycol = mydb["fs.files"]

desc = []

i = 0
f_algo = ' '

#importing images in photos folder to form a orange data table of available images
import_images = ImportImages()
p1 =  os.getcwd() + "/../.."
#path of the stored images 
path = p1 + "/photos"
data, err = import_images(path)   

embeddings = [None] * len(data)
image_file_paths = [None] * (len(data) + 1)


#retieving the embeddings from database depending upon user's selected algorithm
algo = upload.features_algo
u = 0
for i in range(len(data)):
	mydoc = None
	if(algo == 'inception-v3'):
    		f_algo = 'inception-v3'
    		mydoc = mycol.find({"filename":str(data[i,'image'])},{"metadata.annotations": 0, "metadata.vgg16Features": 0, "metadata.vgg19Features": 0 })
	elif(algo == 'vgg16'):
    		f_algo = 'vgg16'
    		mydoc = mycol.find({"filename":str(data[i,'image'])},{"metadata.annotations": 0, "metadata.Inception-v3": 0, "metadata.vgg19Features": 0 })
	else:
    		f_algo = 'vgg19'
    		mydoc = mycol.find({"filename":str(data[i,'image'])},{"metadata.annotations": 0, "metadata.vgg16Features": 0, "metadata.Inception-v3": 0 })
	
	
	if str(data[i,'image']) == 'zzzzzzz.png':
		u = i
	for x in mydoc:
		embeddings[i] = x["metadata"]
		
        
#path of the uploaded image
path2 = p1 + "/WEB-INF/cgi/files/c" + str(upload.cid2)
print(str(upload.cid2))
data_up, err2 = import_images(path2)

image_file_paths = [None] * len(data)

i = 0

for i in range(len(data)):
    image_file_paths[i] = path + "/" +  str(data[i,'image'])


image_file_paths2 = [None] * len(data_up)
for i in range(len(data_up)):
    image_file_paths2[i] = path2 + "/" +  str(data_up[i,'image'])

# extracting features from images (embedding) of uploaded image
from orangecontrib.imageanalytics.image_embedder import ImageEmbedder
with ImageEmbedder(model=f_algo) as emb:
    emb_up = emb(image_file_paths2)


#storing the images of uploaded image in database temporarily (required)
mydb = myclient[upload.db]
mycol = mydb["file_up"]

mycol.update_one({"client_id":upload.cid2},{"$set": { "metadata.features": emb_up[0]}})

#retrieving the just stored featues again
myquery = {"client_id":upload.cid2}
mydoc = mycol.find(myquery)
for x in mydoc:
    embeddings[u] = x["metadata"]
data_2 = data

#getting embeddings for each image as a key value pair
values = []
for dictionary in embeddings:
    values.extend([v for k, v in dictionary.items()])


data2 = ImageEmbedder.prepare_output_data(data_2, values)    

out_data = data2[0]


#selection of distance algorithm by user
d_algo = upload.distance_algo

# computing distance among images
from Orange.distance import Cosine, Euclidean
dist = data2[0]
if(d_algo == 'Cosine'):
    dist_matrix = Cosine(dist)
else:
    dist_matrix = Euclidean(dist)

imf = []

for i in range(len(dist)):
    imf.append(str(dist[i,'image']))

#hierarchical clustering (dividing images into clusters)

groups = {}


from Orange.clustering import hierarchical
hierar = hierarchical.HierarchicalClustering(n_clusters = upload.NumberOfCluster)
hierar.linkage = hierarchical.WARD
hierar.fit(dist_matrix)
#print(hierar.labels)

for file, cluster in zip(imf,hierar.labels):
    if cluster not in groups.keys():
        groups[cluster] = []
        groups[cluster].append(file)
    else:
        groups[cluster].append(file)

#to find out in which cluster the uploaded image went
cluster = 0
c = 0
for x in groups:
    for y in groups[x]:
        c = c + 1
        fi = os.path.basename(image_file_paths2[0])
        fy = os.path.basename(y)
        if(fi == fy):
            cluster = x #cluster to be chosen 
            break

#html code to display output
print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')
print(' <head>')
print('     <meta charset="utf-8">')
print('     <title>Anwendungen im Databanklabor</title>')
print('     <link rel="stylesheet" type="text/css" href="../browser.css">')
print('     <link rel="stylesheet" type="text/css" href="../styles.css">')
print('     <script type="text/javascript" src="../jquery-2.1.1.min.js"></script>')
print('     <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">')
print('     <script src="//code.jquery.com/jquery-1.10.2.js"></script>')
print('     <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>')
print('     <script> function setImg(){')
print('         var imgName = localStorage.getItem("imgName");')
print('         document.getElementById("imgName").innerHTML = imgName;')
print('     }</script>')
print(' </head>')
print('<body>')
print(' <div id="wapper">')
print('     <div id="header">')
print('         <h1 id="headline">Lab DB</h1>')
print('         <nav id="nav_main">')
print('         <a href="/SQLTool/index.html">SQL Tool</a>')
print('         <a href="../index.html" class="currentPage">Image Database</a>')
print('         </nav>')
print('         <div id="logoHSO">')
print('             <a href="http://www.hs-offenburg.de" target="_blank"><img src="../bilder/logoHSO.gif" alt="Hochschule Offenburg"></a>')
print('         </div>')
print('         <img src="../bilder/line_top.png" id="line_top">')
print('     </div>')
print('     <img id="hand" src="../bilder/hand.png">')
print('     <div id="nav_left">')
print('         <div id="menuItem">')
print('             <a href="../index.html" class="currentPage">Image Search</a><br>')
print('             <a href="../Help/index.html">Help</a><br>')
print('             <a href="../Developers/index.html">Developers</a><br>')
print('             <a href="../Admin Login/index.html">Admin Login</a>')
print('         </div>')
print('     </div>')
print('     <div id="content">')
print('         <h2 class="margin-left-50" style="font-size: 20px;">Content Based Image Retrieval</h2>')
print('         <div class="margin-left-50" style="margin-left: 100px">')
end = timer()
t1 = end - start 
print('             <h4>Searched Image:<span id="imgName"></span></h4><br>')
print('             <br> <img id="Img123" src="../files/c' + str(upload.cid2) + '.png" height="100px" width="100px">')
print('             <h4>' +str(len(groups[cluster]) -  1) + ' result(s) in '+ str(round(t1, 2)) +' second(s) <a href="../index.html">Back to Search</a></h4>')
print('         </div>')
print('         <div id="result" class="margin-left-50 scrollbar" style="margin-left: 100px">')
#retrieving the filenames from identified cluster and displaying them with annotations
from subprocess import run
for x in groups[cluster]:
    filename = os.path.basename(x)
    if('zzzzzzz.png' == filename):
        pass
    else:
        myDesc1 = description.getDescription('ImageDB',filename)
        myDesc = str(myDesc1)
        myDesc = myDesc.replace('#', '')
        myDesc = myDesc.replace('\"', '')
        myDesc = re.sub('\d','',myDesc)
        myDesc = myDesc.replace('metadata','')
        myDesc = myDesc.replace('annotations','')
        myDesc = myDesc.replace('{','')
        myDesc = myDesc.replace('}','')
        print('<div class="box" style="display:inline-block; ">')#overflow-y: auto;
        print('     <img src=\'../photos/' + filename + '\' height="200px" width="200px">')
        print('     <div class="overbox" >')
        print('         <div class="tagline overtext"><a href="../photos/'+ filename + '"><br>Download<br><br></a>' + str(myDesc) + '</div>')
        print('     </div>')
        print('</div>')
print('         </div>')
print('     </div>')
print('     <footer>')
print('         <img src="../bilder/line_bottom.png" id="line_bottom">')
print('         <p id="nameProf">Prof. Dr. Volker Sänger, <a id="mail" href="mailto:volker.saenger@hs-offenburg.de">volker.saenger@hs-offenburg.de</a>')
print('         </p>')
print('     </footer>')
print(' </div>')
print('</body>')
print('<img src="https://webanalyse.hs-offenburg.de/piwik.php?idsite=11&rec=1" style="border:0" alt="" />')
print('</html>')

#deleting the temporarily uploaded image and it's embeddings from database         
myquery = { "client_id": upload.cid2 }
mycol.delete_one(myquery)

#from time import sleep
#time.sleep(5)
os.remove('files/c' + str(upload.cid2) + '/zzzzzzz.png')
