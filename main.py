import watchdog.events 
import watchdog.observers 
import time
import requests
import urllib
import json
import os
import cgi
import shutil
  
  
class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self): 
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.txt'], ignore_directories=True, case_sensitive=False) 
  
    def on_created(self, event): 
        ################# UPLOAD PART #################################
        #print("Watchdog received created event - % s." % event.src_path) 
        # Event is created, you can process it now
        #waitingtime that the file is be written
        time.sleep(10)
        url='https://narutohyuuga3.pythonanywhere.com/uploadTXT'
        fin = open(event.src_path, 'rb')
        files = {'text': fin}
        try:
            r = requests.post(url, files=files)
            print('+++++++++++ Upload of '+ event.src_path +' ++++++++++++++++')
            print(r.text)
        finally:
	        fin.close()
        
  
  
if __name__ == "__main__": 
    src_path = r'upload/'
    event_handler = Handler() 
    observer = watchdog.observers.Observer() 
    observer.schedule(event_handler, path=src_path, recursive=True) 
    observer.start() 

    try: 
        with open("database/filelist.json", "r", encoding="utf-8") as file:
            locallist = json.load(file)

        urlDB='https://narutohyuuga3.pythonanywhere.com/downloadFILES'
        urlPCM='https://narutohyuuga3.pythonanywhere.com/return-filesPCM/?PCMkey='
        urlTXT='https://narutohyuuga3.pythonanywhere.com/uploadTXT'

        while True:
            ############### Autodownload Part ###########################
            ## first getting database list to evaluate missing files

            data={'fckwq': 'E-Inhalator-Client_1', 'kdwedu': 'E-Inhalatorprototypenentwicklung-der-Stufe_2!ükx/%'}
            response=requests.post(urlDB, data=data)
            with open("database/serverfilelist.json", 'wb') as s:
                s.write(response.content)

            with open("database/serverfilelist.json", "r", encoding="utf-8") as file:
                audios = json.load(file)

            ## estimating missing files
            missing=[]
            for afile in audios:
                if (afile not in locallist):
                    missing.append(afile)

            ##downloading missing files
            print(missing)
            for download in missing:
                while True:
                    print('############### Downloading '+ download + ' ###################')
                    req = urllib.request.Request(urlPCM + download, method='HEAD')
                    r = urllib.request.urlopen(req)
                    filename = r.info().get_filename()
                    statuscode=r.getcode()
                    print(statuscode)
                    urllib.request.urlretrieve(urlPCM + download, 'download/'+download)
                    print('Dateiname:')
                    print(filename)
                    locallist.append(download)

                    ###sleeping time for matlab-filewatcher & analysation
                    time.sleep(30)
                    if statuscode == 200:
                        print("break")
                        break
    
            print("saving...")
            #saving locallist in filelist.json
            with open("database/filelist.json","w", encoding="utf-8") as file:
                json.dump(locallist, file, ensure_ascii=False, indent=2)
    
            #sleeptime if there was no file to analyze
            if len(missing)<1:
                time.sleep(60)


    except KeyboardInterrupt: 
        observer.stop() 
    observer.join()
    print('End of programm')