import urllib.request
import cgi
import os
import time
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

with open("database/filelist.json", "r", encoding="utf-8") as file:
        locallist = json.load(file)

urlDB='http://narutohyuuga3.pythonanywhere.com/downloadFILES'
urlPCM='http://narutohyuuga3.pythonanywhere.com/return-filesPCM/?PCMkey='
urlTXT='http://narutohyuuga3.pythonanywhere.com/uploadTXT'

while True:
    #Autodownload Part
    ## first getting database list to evaluate missing files

    req = urllib.request.Request(urlDB, method='HEAD')
    r = urllib.request.urlopen(req)
    filename = r.info().get_filename()
    urllib.request.urlretrieve(urlDB, 'database/'+filename)

    with open("database/"+filename, "r", encoding="utf-8") as file:
        audios = json.load(file)

    ## estimating missing files
    missing=[]
    for afile in audios:
        if (afile not in locallist):
            missing.append(afile)

    ##downloading missing files
    print(missing)
    for download in missing:
        print('############### Downloading '+ download + '###################')
        req = urllib.request.Request(urlPCM+download, method='HEAD')
        r = urllib.request.urlopen(req)
        filename = r.info().get_filename()
        urllib.request.urlretrieve(urlPCM+download, 'download/'+filename)
        print('Dateiname:')
        print(filename)
        locallist.append(download)
        
        ###sleeping time for matlab-filewatcher & analysation
        '''maybe wait for new file created in upload'''
        #Autoupload Part
        ## -> Filewatcher on /upload/file.txt

        ## -> upload part
    

    #saving locallist in filelist.json
    with open("database/filelist.json","w", encoding="utf-8") as file:
        json.dump(locallist, file, ensure_ascii=False, indent=2)
    
    #sleeptime
    time.sleep(15)

print('End of programm')