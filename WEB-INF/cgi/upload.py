import cgi, os
import cgitb; cgitb.enable()
from PIL import Image
import pymongo
import random


form = cgi.FieldStorage()
cid2 = 0
# A nested FieldStorage instance holds the file
fileitem = form['file']
NumberOfCluster = int(form.getvalue('slider'))

#database to be used
db = 'ImageDB'
port = '27018'
features_algo = form.getvalue('features_algo')
distance_algo = form.getvalue('distance_algo')


# Test if the file was uploaded
if fileitem.filename:

    # strip leading path from file name
    # to avoid directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    
    did = ""
    def randNum():
        #assigning id to connected client (user)
        cid = random.randint(1,100000)
        
        
        myclient = pymongo.MongoClient("mongodb://localhost/")
        mydb = myclient[db]
        mycol = mydb["file_up"]

        myquery = {"client_id":cid}
        res = mycol.find(myquery)

        if res == cid:
            #check if user with same id exists, if yes recall the function 
            randNum()
        else:
            #storing connected client id in database temporarily
            mydict = {"metadata":{"features":"a"}, "client_id": cid}
            x = mycol.insert_one(mydict)
            di = 'files/c' + str(cid) + '/'
            os.makedirs(di)
            open(di + fn, 'wb').write(fileitem.file.read())
            from shutil import copyfile
            # loops through the Input Image file
            current_img = Image.open(di + fn)

            # coverts the images to PNG + saves to the output folder
            current_img.save(di + 'zzzzzzz' + '.png', 'PNG')
            did = di
            from shutil import copyfile
           
            copyfile(di + 'zzzzzzz.png', '../../photos/zzzzzzz.png')
            copyfile(di + 'zzzzzzz.png', '../../files/c' + str(cid) + '.png')
            os.remove(di + fn)
            cid2 =cid
            return cid

 
    cid2 = randNum()

else:
    message = 'No file was uploaded'

