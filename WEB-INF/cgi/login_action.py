import cgi, os
import cgitb; cgitb.enable()
import pymongo

db = 'ImageDB'
myclient = pymongo.MongoClient("mongodb://localhost/")
mydb = myclient[db]
mycol = mydb["login"]

#reading data from form
form = cgi.FieldStorage()

#geting values posted by admin login form
login_id = form.getvalue('username') 	
password = form.getvalue('password')


print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')

myquery = {"login_id":login_id}
o1 = mycol.find_one({},{"_id":0})
path = os.getcwd() + "/../../files"
url = ' '
#authenticating admin details
if o1['login_id'] == login_id and o1['password'] == password:
	url = "../Admin Login/seite1.html"
	import os, shutil
	import glob

	#removing uploaded image and annotation file
	files = glob.glob(path + '/*.png')
	for f in files:
		os.remove(f)
else:
	url = "../Admin Login/index.html"

print('<meta http-equiv="refresh" content="0; url=' + url + '" />')




print('</html>')