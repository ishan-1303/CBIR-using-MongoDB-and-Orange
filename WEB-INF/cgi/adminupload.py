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

di = '../../uploaded/'

port = '27018'
db = 'ImageDB'
newfile = []
annotations = []
ids = []



myclient = pymongo.MongoClient("mongodb://localhost/")
mydb = myclient[db]
mycol = mydb["fs.files"]

#function to upload image into database
def uploadImages():
	i = 0
	for x in fileitems:
		if i == 0:
			iid = random.randint(1,100000) #assigning random Id to image
		
		myquery = {"id":iid}
		res = mycol.find(myquery)
		#if id is already assigned then recall the function
		if res == iid:
			uploadImages()
		else:

			nf = 'y' + str(iid)
			ext = os.path.splitext(x.filename)[-1].lower()
			fn = os.path.basename(x.filename)
			open(di + fn, 'wb').write(x.file.read())
			if x.filename:
				if ext == '.txt':
					#logic behind storing annotation file temporarily 
					os.rename(di + fn, di + 'annotations/' + nf + '.txt') #renaming uploaded annotation file
					annotations.append(nf + '.txt')
					i = i - 1
				else:
					#logic behind saving image into photos folder of project (where all images are stored permanantly)
					current_img = Image.open(di + fn)
					current_img.save(di + 'y' + str(iid) + '.png', 'PNG')
					newfile.append('y' + str(iid) + '.png')
					ids.append(str(iid))
					copyfile(di + 'y' + str(iid) + '.png', os.getcwd() + '/../../photos/y' + str(iid) + '.png') #renaming uploaded image
					i = i + 1
					os.remove(di + fn)	#removing the uploaded file after it is pasted in photos folder
			
uploadImages()
directory = os.getcwd() + '/../../uploaded'

print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')
#to store uploaded image into database
from subprocess import run
for filename in os.listdir(directory):
	if filename.endswith(".png"):
		run(["/usr/bin/mongofiles", "-d", db, "-l", os.path.join(directory, filename), "put", filename]) #C:\\Program Files\\MongoDB\\Server\\4.2\\bin\\mongofiles.exe
			#path of mongofiles

mydb = myclient[db]
mycol = mydb["fs.files"]

i = 0

#to set image id for uploaded image
for x in newfile:
	myquery = {"filename": x}
	newvalues = { "$set": { "id": ids[i]} } 
	mycol.update_one(myquery, newvalues)
	i = i + 1
print('</html>')
