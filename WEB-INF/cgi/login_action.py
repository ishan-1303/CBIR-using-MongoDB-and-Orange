import cgi, os
import cgitb; cgitb.enable()
import pymongo

db = 'ImageDB'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["login"]

form = cgi.FieldStorage()

login_id = form.getvalue('username')
password = form.getvalue('password')


print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')
#print(login_id + ' ' + password)

myquery = {"login_id":login_id}
o1 = mycol.find_one({},{"_id":0})
#print(o1)
url = ' '
if o1['login_id'] == login_id and o1['password'] == password:
	url = "../Admin Login/seite1.html"
else:
	url = "../Admin Login/index.html"

print('<meta http-equiv="refresh" content="0; url=' + url + '" />')




print('</html>')