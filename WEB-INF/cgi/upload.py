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
db = 'ImageDB'
features_algo = form.getvalue('features_algo')
distance_algo = form.getvalue('distance_algo')


# Test if the file was uploaded
if fileitem.filename:

    # strip leading path from file name
    # to avoid directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    
   # message = 'The file "' + fn + '" was uploaded successfully'
    
    #copyfile('files/zzzzzzz.png', 'files/zzzzzzz.png')
    
    did = ""
    def randNum():
        
        cid = random.randint(1,100000)
        
        
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db]
        mycol = mydb["file_up"]

        myquery = {"client_id":cid}
        res = mycol.find(myquery)

        if res == cid:
            randNum()
        else:
            mydict = {"metadata":{"features":"a"}, "client_id": cid}
            x = mycol.insert_one(mydict)
            di = 'files/c' + str(cid) + '/'
            os.makedirs(di)
            open(di + fn, 'wb').write(fileitem.file.read())
            from shutil import copyfile
            # loops through the InputJPG
            current_img = Image.open(di + fn)

            #print('Working on image: ' + os.path.splitext(filename)[0])
            #print(   f'Format: {current_img.format}, Size: {current_img.size}, Mode: {current_img.mode}')

            # coverts the images to PNG + saves to the output folder
            current_img.save(di + 'zzzzzzz' + '.png', 'PNG')
            did = di
            from shutil import copyfile
            # copyfile('files/' + fn, 'files/zzzzzzz.png')
            copyfile(di + 'zzzzzzz.png', '../../photos/zzzzzzz.png')
            copyfile(di + 'zzzzzzz.png', '../../files/c' + str(cid) + '.png')
            os.remove(di + fn)
            cid2 =cid
            return cid

 
    cid2 = randNum()

else:
    message = 'No file was uploaded'

