import os
import sys
from threading import Thread
from pathlib import Path
import time

# print("len(sys.argv)",len(sys.argv))
if len(sys.argv) != 4:
    print("usage : go.py  <repIn>  <repOut>  <vidéosEntrelacées 0|1>")
    exit(1)

nmPgm               =sys.argv[0]
rin                 =sys.argv[1]
rout                =sys.argv[2]
vidéosEntrelacées   =sys.argv[3]

r=os.path.join(rin, rout)
if not os.path.exists(r):
    print("Création de",r)
    os.makedirs(r)

entrees = os.listdir(rin)

# https://waytolearnx.com/2020/06/les-threads-en-python.html
def job(args):
    print("Le thread est en veille ", args[0])
    # time.sleep(2)
    os.system(args[1])
    print("Le thread s'est réveillé", args[0])
    
i=0

for entree in entrees:
    i+=1
    f=os.path.join(rin, entree)
    if os.path.isfile(f):
        # print("[F]",entree)
        stem=Path(f).stem
        suffix=Path(f).suffix
        # print("stem:",stem)
        # print("suffix:",suffix) 
        if suffix.lower() ==  '.mts':
            # print("[F à traiter]" ,entree, end = '\n')
            fOut = os.path.join(rin, rout, stem+".mp4")
            if vidéosEntrelacées == "1":
                s = "ffmpeg -hide_banner -loglevel error -i " + '"'+fIn+'"' + " -vf yadif " + '"'+fOut+'"';
            else:
                s = "ffmpeg -hide_banner -loglevel error -i " + '"'+f+'"' + "  " + '"'+fOut+'"';
            print(s)
            
            # t = Thread(target=job, args=([i,s],))
            # t.start()
            
            os.system(s)

