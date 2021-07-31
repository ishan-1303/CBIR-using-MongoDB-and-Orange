import os

directory = os.getcwd() + "/photos" #"I:\\Tomcat\\webapps\\proui\\uploaded" 


print('Content-type:text/html\n\n')
print('<!DOCTYPE html>')
print('<html>')
db = 'ImageDB'
from subprocess import run
for filename in os.listdir(directory):
    if filename.endswith(".png"):
    	run(["C:\\Program Files\\MongoDB\\Server\\4.2\\bin\\mongofiles.exe","-d", db, "-l", os.path.join(directory, filename), "put", filename]) #C:\\Program Files\\MongoDB\\Server\\4.2\\bin\\mongofiles.exe
    	print('uploaded <br>')

print('</html>')

 
