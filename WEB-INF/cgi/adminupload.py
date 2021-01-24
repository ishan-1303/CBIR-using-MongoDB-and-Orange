import cgi, os
import cgitb; cgitb.enable()
from PIL import Image
import pymongo
import random
from shutil import copyfile

form = cgi.FieldStorage()
iid = 0
# A nested FieldStorage instance holds the file
fileitems = form['files']

di = '..\\..\\uploaded\\'

db = 'test3'
newfile = []
annotations = []
ids = []



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]


def uploadImages():
	i = 0
	for x in fileitems:
		if i == 0:
			iid = random.randint(1,100000)
		
		myquery = {"id":iid}
		res = mycol.find(myquery)
		if res == iid:
			uploadImages()
		else:
			nf = 'y' + str(iid)
			ext = os.path.splitext(x.filename)[-1].lower()
			fn = os.path.basename(x.filename)
			open(di + fn, 'wb').write(x.file.read())
			if x.filename:
				if ext == '.txt':
					os.rename(di + fn, di + 'annotations\\' + nf + '.txt')
					annotations.append(nf + '.txt')
					i = i - 1
					#os.remove(di + 'annotations\\' + fn)
				else:
					current_img = Image.open(di + fn)
					current_img.save(di + 'y' + str(iid) + '.png', 'PNG')
					newfile.append('y' + str(iid) + '.png')
					ids.append(str(iid))
					copyfile(di + 'y' + str(iid) + '.png', os.getcwd() + '\\..\\..\\photos\\y' + str(iid) + '.png')
					i = i + 1
					os.remove(di + fn)
			
uploadImages()
directory = os.getcwd() + '\\..\\..\\uploaded'

print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')
from subprocess import run
for filename in os.listdir(directory):
	if filename.endswith(".png"):
		run(["\\usr\\bin", "-d", db, "-l", os.path.join(directory, filename), "put", filename]) #C:\\Program Files\\MongoDB\\Server\\4.2\\bin\\mongofiles.exe
		#print('uploaded <br>')

mydb = myclient[db]
mycol = mydb["fs.files"]

i = 0

for x in newfile:
	myquery = {"filename": x}
	newvalues = { "$set": { "id": ids[i]} } 
	mycol.update_one(myquery, newvalues)
	i = i + 1
print('</html>')
