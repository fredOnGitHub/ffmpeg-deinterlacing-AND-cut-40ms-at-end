import os
import sys
import subprocess
import time
from threading import Thread

#for arg in sys.argv:
#    print (arg)
##############################################################################
def Clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def est_rep(r):
    if os.path.exists(r):
        return True
    return False

##############################################################################
#https://www.developpez.net/forums/d1300528/autres-langages/python/general-python/listing-recursif-repertoire-x-niveaux/
def contenurep(rep, rout, vidéosEntrelacées, nivmax=0, nivcour=1):
    entrees = os.listdir(rep)
    entrees.sort(key=lambda v: v.upper()) # tri sans tenir compte de la casse
    sousrep = [] # recevra les noms des sous-répertoires
    sousfic = [] # recevra les noms des fichiers
    for entree in entrees:
        if os.path.isdir(os.path.join(rep, entree)):
            sousrep.append(entree)
        else:
            sousfic.append(entree)

    print ("\nDans le rép",rep," :")
    for srep in sousrep:
        print ("[R]", srep)

    repTest=os.path.join(rep, rout)
    print("Test de ",repTest)
    if not os.path.exists(repTest):
        print("Création de",repTest)
        os.makedirs(repTest)

    for sfic in sousfic:
        filename=os.path.splitext(sfic)[0]
        extension=os.path.splitext(sfic)[1]
        # print("filename:",filename)
        # print("extension:",extension)
        if extension.lower() ==  '.mts':
            # print("[F à traiter]" ,sfic, end = '\n')
            fIn = os.path.join(rep, sfic)
            fOut = os.path.join(rep, rout, filename+".mp4")
            # print('vidéosEntrelacées:',vidéosEntrelacées)

            # mettre en silence la sortie de ffmpeg
            # https://superuser.com/questions/326629/how-can-i-make-ffmpeg-be-quieter-less-verbose
            if vidéosEntrelacées == "1":
                s = "ffmpeg -hide_banner -loglevel error -i " + '"'+fIn+'"' + " -vf yadif " + '"'+fOut+'"';
            else:
                s = "ffmpeg -hide_banner -loglevel error -i " + '"'+fIn+'"' + "  " + '"'+fOut+'"';
            print(s)
            os.system(s)

            # if vidéosEntrelacées == "1":
                # t=["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", fIn, "-vf", "yadif", fOut]
            # else:
                # t=["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", fIn, fOut]
            # print(t)
            # subprocess.call(t)

    # appel récursif si demandé
    if nivmax==0 or nivcour<nivmax:
        for srep in sousrep:
            contenurep(os.path.join(rep, srep), rout, vidéosEntrelacées, nivmax, nivcour+1)

# print("len(sys.argv)",len(sys.argv))
if len(sys.argv) != 4:
    print("usage : go.py  <repIn>  <repOut>  <vidéosEntrelacées 0|1>")
    exit(1)

nmPgm               =sys.argv[0]
rin                 =sys.argv[1]
rout                =sys.argv[2]
vidéosEntrelacées   =sys.argv[3]

Clean()
t0=time.perf_counter()
contenurep(rin, rout, vidéosEntrelacées, 0, 1)#pas d'appel rec avec 1, 1
t1=time.perf_counter()
print("temps total : ",t1-t0)
