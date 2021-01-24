import Orange
import pymongo
import os
# importing images
import upload
from orangecontrib.imageanalytics.import_images import ImportImages
#import featuresfromdb
import description
import re

import time
t0= time.clock()

#image_file_paths = featuresfromdb.image_file_paths

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[upload.db]
mycol = mydb["fs.files"]

desc = []

i = 0
embeddings = []
image_file_paths = []
f_algo = ' '
#1vgg16Features
#2vgg19Features
#3Inception-v3

if(upload.features_algo == 'inception-v3'):
    f_algo = 'inception-v3'
    mydoc = mycol.find({},{"metadata.annotations": 0, "metadata.vgg16Features": 0, "metadata.vgg19Features": 0 }).sort("filename")
elif(upload.features_algo == 'vgg16'):
    f_algo = 'vgg16'
    mydoc = mycol.find({},{"metadata.annotations": 0, "metadata.Inception-v3": 0, "metadata.vgg19Features": 0 }).sort("filename")
else:
    f_algo = 'vgg19'
    mydoc = mycol.find({},{"metadata.annotations": 0, "metadata.vgg16Features": 0, "metadata.Inception-v3": 0 }).sort("filename")



        


for x in mydoc:
    embeddings.append(x["metadata"])
    image_file_paths.append(x["filename"])

import_images = ImportImages()
p1 =  os.getcwd() + "\\..\\.."
path = p1 + "\\photos"
data, err = import_images(path)    

path2 = p1 + "\\WEB-INF\\cgi\\files\\c" + str(upload.cid2)
print(str(upload.cid2))
data_up, err2 = import_images(path2)
#print(data_up) 
image_file_paths = [None] * len(data)
i = 0
for i in range(len(data)):
    image_file_paths[i] = path + "\\" +  str(data[i,'image'])


image_file_paths2 = [None] * len(data_up)
for i in range(len(data_up)):
    image_file_paths2[i] = path2 + "\\" +  str(data_up[i,'image'])

# extracting features from images (embedding)
from orangecontrib.imageanalytics.image_embedder import ImageEmbedder
with ImageEmbedder(model=f_algo) as emb:
    emb_up = emb(image_file_paths2)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[upload.db]
mycol = mydb["file_up"]

mycol.update_one({"client_id":upload.cid2},{"$set": { "metadata.features": emb_up[0]}})

myquery = {"client_id":upload.cid2}
mydoc = mycol.find(myquery)
for x in mydoc:
    embeddings.append(x["metadata"])
data_2 = data

values = []
for dictionary in embeddings:
    values.extend([v for k, v in dictionary.items()])


data2 = ImageEmbedder.prepare_output_data(data_2, values)    

out_data = data2[0]


# computing distance among images
d_algo = upload.distance_algo

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


cluster = 0
c = 0
for x in groups:
    for y in groups[x]:
        c = c + 1
        fi = os.path.basename(image_file_paths2[0])
        fy = os.path.basename(y)
        if(fi == fy):
            cluster = x
            break

print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')
print(' <head>')
print('     <meta charset="utf-8">')
print('     <title>MI-Learning</title>')
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
print('             <a href="../Project Supervisor/index.html">Project Supervisor</a><br>')
print('             <a href="../Admin Login/index.html">Admin Login</a>')
print('         </div>')
print('     </div>')
print('     <div id="content">')
print('         <h2 class="margin-left-50" style="font-size: 20px;">Content based Image Retrieval</h2>')
print('         <div class="margin-left-50" style="margin-left: 100px">')
t1 = time.clock() - t0
t1 = str(round(t1,2))
print('             <h4>Searched Image:<span id="imgName"></span></h4><br>')
print('             <br> <img id="Img123" src="../files/c' + str(upload.cid2) + '.png" height="100px" width="100px">')
print('             <h4>' +str(len(groups[cluster]) -  1) + ' result(s) in '+str(t1)+' second(s) <a href="../index.html">Back to Search</a></h4>')
print('         </div>')
print('         <div id="result" class="margin-left-50 scrollbar" style="margin-left: 100px">')
# print('        <div style="float : left;">')
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
        #print('         <div class="title overtext">Ishan</div>')
        print('         <div class="tagline overtext"><a href="../photos/'+ filename + '"><br>Download<br><br></a>' + str(myDesc) + '</div>')
        print('     </div>')
        print('</div>')
# print('</div>')
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
         
myquery = { "client_id": upload.cid2 }
mycol.delete_one(myquery)

from time import sleep
time.sleep(5)
os.remove('files/c' + str(upload.cid2) + '/zzzzzzz.png')
# os.remove('C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/proui/photos/zzzzzzz.png')
