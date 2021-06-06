import requests, json, urllib, io

with open("database/filelist.json", "r", encoding="utf-8") as file:
    locallist = json.load(file)

urlDB='http://narutohyuuga3.pythonanywhere.com/downloadFILES'
urlPCM='http://narutohyuuga3.pythonanywhere.com/return-filesPCM/?PCMkey='
urlTXT='http://narutohyuuga3.pythonanywhere.com/uploadTXT'

############### Autodownload Part ###########################
## first getting database list to evaluate missing files
#data=urllib.parse.urlencode({'fckwq': 'E-Inhalator-Client_1', 'kdwedu': 'E-Inhalatorprototypenentwicklung-der-Stufe_2!ükx/%'}).encode()
data={'fckwq': 'E-Inhalator-Client_1', 'kdwedu': 'E-Inhalatorprototypenentwicklung-der-Stufe_2!ükx/%'}
response=requests.post(urlDB, data=data)
with open("database/filelist.json", 'wb') as s:
    s.write(response.content)