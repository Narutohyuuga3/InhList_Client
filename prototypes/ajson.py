import json

audios=['Bobbsy.jpg', 'Joshi.plg']
filename='Kater.pcm'


audios.append(filename)
jsonStr=json.dumps(audios)

print(audios)
print(jsonStr)

missing=[]
localList=['Bobbsy.jpg']
for afile in audios:
    if (afile not in localList):
        missing.append(afile)

print(missing)
