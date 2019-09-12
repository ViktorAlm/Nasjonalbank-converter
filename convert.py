from collections import OrderedDict
d= OrderedDict()

import fileinput
import os
import shutil
from pydub import AudioSegment
from subprocess import call
import concurrent.futures
from multiprocessing import Pool
# [rest of code]

'''
Goes thorugh all folders and add spls(file info) and wav to their lists
'''
def runFileList(folders, wavs, spls):
    data = {}
    for folder in folders:
        data, wavs, spls = openFolderStations(folder, data, wavs, spls)
    return wavs, spls

'''
Since wavs sometimes are in different locations this is a very ugly hack to go through them all
'''
def getWavLocations(adb_folder, data):
    lvl1s = os.listdir(adb_folder)
    for lvl1 in lvl1s:
        lvl2s = os.listdir(adb_folder + "/" +lvl1)
        for lvl2 in lvl2s:
            lvl3s = os.listdir(adb_folder  + "/" + lvl1 + "/" + lvl2)
            for lvl3 in lvl3s:
                lvl4s = os.listdir(adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3)
                for lvl4 in lvl4s:
                    if ".wav" in lvl4:
                        data[lvl3] = adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3
                    else:
                        lvl5s = os.listdir(adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3 + "/" + lvl4)
                        for lvl5 in lvl5s:
                            if ".wav" in lvl5:
                                data[lvl4] = adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3 + "/" + lvl4
                            else:
                                lvl6s = os.listdir(adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3 + "/" + lvl4 + "/" + lvl5)
                                for lvl6 in lvl6s:
                                    if ".wav" in lvl6:
                                        data[lvl5] = adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3 + "/" + lvl4 + "/" + lvl5
    return data

'''
Also incredibly ugly hack for going through the folders
'''
def getSPLLocations(adb_folder, data):
    lvl1s = os.listdir(adb_folder)
    for lvl1 in lvl1s:
        lvl2s = os.listdir(adb_folder + "/" +lvl1)
        for lvl2 in lvl2s:
            lvl3s = os.listdir(adb_folder  + "/" + lvl1 + "/" + lvl2)
            for lvl3 in lvl3s:
                if ".spl" in lvl3:
                    print(lvl3)
                    data[lvl3.split(".")[0]] = adb_folder  + "/" + lvl1 + "/" + lvl2+ "/" + lvl3
                else:
                    lvl4s = os.listdir(adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3)
                    for lvl4 in lvl4s:
                        if ".spl" in lvl4:
                            print(lvl4)
                            data[lvl4.split(".")[0]] = adb_folder  + "/" + lvl1 + "/" + lvl2 + "/" + lvl3+ "/" + lvl4

    return data

'''
Get the information out from a spl by providing its location
'''
def readSPL(splloc):
    RecordSession = ""
    Speaker_ID = 0
    Name = ""
    Sex = ""
    RegionOfBirth = ""
    RegionOfYouth = ""
    Remarks = ""
    paths = []
    texts = []
    readingFiles = False


    if os.path.exists(splloc):
        Speaker_ID = 0
        Name = ""
        Sex = ""
        RegionOfBirth = ""
        RegionOfYouth = ""
        Remarks = ""
        readingFiles = False

        with open(splloc, encoding="windows-1252") as fp:
           line = fp.readline()
           cnt = 1
           while line:
               if "[End]" in line:
                   readingFiles = False
               if(readingFiles):
                   lineSplit = line.split("=")
                   if(len(lineSplit) > 1):
                       op = 2
                       paths.append(lineSplit[1].split(">-<")[9])
                       texts.append(lineSplit[1].split(">-<")[0])


               if "Record session=" in line:
                   RecordSession = line.split("=")[1].replace("\n", "")
               if "1=Speaker ID" in line:
                   Speaker_ID = line.split(">-<")[1].replace("\n", "")
               if "2=Name" in line:
                   Name = line.split(">-<")[1].replace("/", " ").replace("\n", "")
               if "3=Age" in line:
                   Age = line.split(">-<")[1].replace("\n", "")
               if "4=Sex" in line:
                   Sex = line.split(">-<")[1].replace("\n", "")
               if "5=Region of Birth" in line:
                   RegionOfBirth = line.split(">-<")[1].replace("\n", "")
               if "6=Region of Youth" in line:
                   RegionOfYouth = line.split(">-<")[1].replace("\n", "")
               if "7=Remarks" in line:
                   Remarks = line.split(">-<")[1].replace("\n", "")
               if "[Validation states]" in line:
                   readingFiles = True

               ##print("Line {}: {}".format(cnt, line.strip()))
               line = fp.readline()
               cnt += 1
    else:
        rekotkero = 2
        #print("Does no t exists")
        #print(loc)
        #print(speachLoc)
    return Name, Speaker_ID, RecordSession, paths, texts

'''
    The dataset was recorded on different stations. This goes through the stations.
'''
def openFolderStations(folder, data, wavs, spls, lang="swe"):
    authors = []
    stations = os.listdir(folder)
    if lang is "nor":
        setname = folder[9:13]
    if lang is "swe"
        setname = folder[:4]
    #print(setname)
    #print(os.listdir(folder))
    for station in stations:
        #print(folder + station)
        recordings = os.listdir(folder + station)
        #print(os.listdir(folder + station))
        for recording in recordings:
            #print(folder + station+"/"+recording)
            #print(os.listdir(folder + station+"/"+recording))
            adb_folder = folder + station +"/"+ recording + "/adb_"+setname
            print(os.listdir(adb_folder))
            if os.path.exists(adb_folder+"/speech"):
                wavs = getWavLocations(adb_folder+"/speech", wavs)
            if os.path.exists(adb_folder+"/data"):
                spls = getSPLLocations(adb_folder+"/data", spls)
    return data, wavs, spls


if __name__ == "__main__":
    wavs = {}
    spls = {}
    Name = ""
    RecordSession = ""
    Speaker_ID = ""
    paths = []
    texts = []
    if not os.path.exists("swe_nor"):
        os.mkdir("swe_nor")

    wavs, spls = runFileList(["0467 sv train 1/", "0467 sv train 2/", "0467 sv train 3/", "0468 sv test/"], wavs, spls)
#    wavs, spls = runFileList(["no.16khz.0463-1/", "no.16khz.0463-2/", "no.16khz.0463-3/", "no.16khz.0463-4/", "no.16khz.0464-testing/"], wavs, spls)
    print("starting with: " + str(len(wavs.keys())) + " authors")
    count = 0
    for knownWav in wavs.keys():
        Name, Speaker_ID, RecordSession, paths, texts = readSPL(spls[knownWav])
        Speaker_ID = str(Name.replace(" ", ""))
        print(str(count) + ". working on: " + knownWav + " by " + Speaker_ID + "in " +wavs[knownWav])
        if not os.path.exists("swe_nor/"+Speaker_ID):
            os.mkdir("swe_nor/"+Speaker_ID)
        if not os.path.exists("swe_nor/"+Speaker_ID+"/"+RecordSession):
            os.mkdir("swe_nor/"+Speaker_ID+"/"+RecordSession)
        totalFiles = 0
        for file in paths:
            if(os.path.isfile(wavs[knownWav]+"/"+file) and "001.wav" not in file and totalFiles < 15):
                print("coyping: "+wavs[knownWav]+"/"+file)
                concall1 = "ffmpeg -f s16le -ar 16k -ac 2 -i "
                concall2 = " -map_channel 0.0.1 -ar 16k -ss 00:00.2 "
                call(concall1 + '"' + wavs[knownWav] + "/" + file + '"' +  concall2 + '"' + "swe_nor/"+Speaker_ID+"/"+RecordSession+"/"+file + '"', shell=True)
                totalFiles = totalFiles+1
        count= count+1
        with open("swe_nor/"+Speaker_ID+"/"+RecordSession+"/texts", 'a') as file:
            for i, j in zip(paths, texts):
                if(os.path.isfile(wavs[knownWav]+"/"+i) and "001.wav" not in i):
                    file.write(i[:-4]+" " +j+"\n")
