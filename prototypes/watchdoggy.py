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
        print("Watchdog received created event - % s." % event.src_path) 
        # Event is created, you can process it now
        url='http://narutohyuuga3.pythonanywhere.com/uploadTXT'
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
        pass
    except KeyboardInterrupt: 
        observer.stop() 
    observer.join()
    print('End of programm')