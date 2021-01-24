import pymongo
import cgi
import os
import socket

import time
t0= time.clock()
		

form = cgi.FieldStorage()
searchterm =  form.getvalue('searchBox')
db = "ImageDB"


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]



myquery = {"$text": {"$search": searchterm}}
#mydoc = mycol.distinct('filename')
mydoc = mycol.find(myquery)
i = 0;

t1 = time.clock() - t0


print('Content-type:text/html\n\n')



print('<!DOCTYPE html>')
print('<html>')

print('<head>')
print('<meta charset="utf-8">')
print('<title>MI-Learning</title>')

print('<link rel="stylesheet" type="text/css" href="../browser.css">')
print('<link rel="stylesheet" type="text/css" href="../styles.css">')
print('<script type="text/javascript" src="../jquery-2.1.1.min.js"></script>')

print('<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">')
print('<script src="//code.jquery.com/jquery-1.10.2.js"></script>')
print('<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>')
print('<script>')
print('var imgName = localStorage.getItem("imgName");')
print('document.getElementById("imgName").innerHTML = imgName;')
print('</script>')

print('</head>')

print('<body >')
print('<div id="wapper">')
print('<div id="header">')
print('<h1 id="headline">Lab DB</h1>')

print('<nav id="nav_main">')
print('<a href="/SQLTool/index.html">SQL Tool</a>')
print('<a href="../index.html" class="currentPage">Image Database</a>')

print('</nav>')
print('<div id="logoHSO">')
print('<a href="http://www.hs-offenburg.de" target="_blank"><img src="../bilder/logoHSO.gif" alt="Hochschule Offenburg"></a>')
print('</div>')
print('<img src="../bilder/line_top.png" id="line_top">')
print('</div>')
print('<img id="hand" src="../bilder/hand.png">')

print('<div id="nav_left">')
print('<div id="menuItem">')
print('<a href="../index.html"class="currentPage">Image Search</a><br>')
print('<a href="../Help/index.html">Help</a><br>')
print('<a href="../Developers/index.html">Developers</a><br>')
print('<a href="../Project Supervisor/index.html">Project Supervisor</a><br>')
print('<a href="../Admin Login/index.html">Admin Login</a>')
print('</div>')

print('</div>')

print('<div id="content">')

print('<h2 class="margin-left-50" style="font-size: 20px;">Content based Image Retrieval</h2>')
print('<div class="margin-left-50" style="margin-left: 100px">')

# print(db)
t1 = time.clock() - t0
t1 = str(round(t1,2))
# print('<h5>Image Name: <span id="imgName"></span></h5>')
#print('<input type="button" class="pointer btns" onclick="submitForm()" value="New Search" style="margin-left:450px; margin-top:-125px;">')
print('<h4>' + str(mydoc.count()) + ' results for ' + searchterm + ' in ' + str(t1) + ' seconds <a href="../index.html">Back to Search</a></h4>')
print('</div>')
print('<div id="result" class="margin-left-50 scrollbar" style="margin-left: 100px; height:450px">')
from subprocess import run
for x in mydoc:
	filename = os.path.basename(x["filename"])
	print('<img src=\'../photos/' + filename + '\' height="150px" width="150px">')
print('</div>')
print('</div>')
print('<footer>')
print('<img src="../bilder/line_bottom.png" id="line_bottom">')
print('<p id="nameProf">Prof. Dr. Volker Sänger, <a id="mail" href="mailto:volker.saenger@hs-offenburg.de">volker.saenger@hs-offenburg.de</a>')
print('</p>')
print('</footer>')
print('</div>')

print('</body>')

print('<img src="https://webanalyse.hs-offenburg.de/piwik.php?idsite=11&rec=1" style="border:0" alt="" />')
print('</html>')
         

# os.remove('C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/proui/photos/zzzzzzz.png')

