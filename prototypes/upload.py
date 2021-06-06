#Testfile for implementing POST-Request
# to the server for uploading a file

import requests

url='http://narutohyuuga3.pythonanywhere.com/uploadTXT'

fin = open('Bobbsy.jpg.txt', 'rb')
files = {'text': fin}
try:
    r = requests.post(url, files=files)
    print(r.text)
finally:
	fin.close()

