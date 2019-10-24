import os
import shlex
import json
import time
import subprocess
import multiprocessing

#Configurable variables
use_ini_file = False                #Allows values in the settings.ini file to overide hardcoded variables
path         = 'z:\\TV Shows\\'     #Root directory for the getListOfFiles method. All sub-directories will be recursively searched for all files

#Non-configurable variables
fileList = []          #Unfiltered fileList
jsonList = []          #Stores JSON output for every file in filteredFileList

#Generates settings.ini file if missing and use_ini_file is set to True
#TODO def generateINI

#Loads the settings from the settings.ini file
#TODO def loadINI

#Recursively searches for files in the given path (root directory)
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = []
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

#Uses ffprobe to get file info and returns info in JSON format
def getVideoMetadata(pathToVideo):
    cmd = "ffprobe.exe -v quiet -print_format json -show_streams -show_format"
    args = shlex.split(cmd)
    args.append(pathToVideo)
    # run the ffprobe process, decode stdout into utf-a and convert to JSON
    try:
        ffprobeOutput = subprocess.check_output(args).decode('utf-8')
        ffprobeOutput = json.loads(ffprobeOutput)
    except:
        print("Error, incompatible file format detected at location " + pathToVideo)
        ffprobeOutput = "ERROR"
    return ffprobeOutput

def getJson(index, fileList, return_list):
    path = fileList[index]
    data = getVideoMetadata(path)
    if (data == "ERROR"):
        print("test")
    else:
        data = json.dumps(data)
        return_list.append = data

# def getJsonList(fileList):
#     list = []
#     length = len(fileList)
#     for index, i in enumerate(fileList):
#         json = getVideoMetadata(i)
#         if (json == "ERROR"):
#             continue
#         list.append(json)
#         print("File " + str(index) + " of " + str(length), end='\r', flush=True)
#     return list

if __name__ == '__main__':
    print("Getting list of all files")
    print()
    fileList = getListOfFiles(path)
    print("Running ffprobe and converting to JSON")
    print()
    manager = multiprocessing.Manager()
    return_list = manager.list()
    jobs = []
    length = len(fileList)
    for index, i in enumerate(fileList):
        p = multiprocessing.Process(target=getJson, args=(index, fileList, return_list))
        jobs.append(p)
        p.start()
        print("Processing file " + str(index) + " of " + str(length), end='\r', flush=True)

    for proc in jobs:
        proc.join()

    print(return_list[0])

# if True:
#     for i in return_list:
#         print (i)
#         # If wanted to print each line by line
#         print ()