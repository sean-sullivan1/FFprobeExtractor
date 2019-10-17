import os
import shlex
import json
import time
import subprocess

#Configurable variables
use_ini_file         = False                #Allows values in the settings.ini file to overide hardcoded variables
path                 = 'z:\\TV Shows\\'     #Root directory for the getListOfFiles method. All sub-directories will be recursively searched for all files
extensionWhiteList   =("mp4","mkv","avi")   #Defines which file extensions will be white listed

#Non-configurable variables
fileList         = []          #Unfiltered fileList
filteredFileList = []          #Filtered fileList
jsonList         = []          #Stores JSON output for every file in filteredFileList

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

#Filters fileList to only contain file with white listed extensions
def filterList(list):
	filteredList = []
	for i in list:
		fileExtension = i[-3:].upper()
		for j in extensionWhiteList:
			if fileExtension == j.upper():
				filteredList.append(i)
	return filteredList

#Uses ffprobe to get file info and returns info in JSON format
def getVideoMetadata(pathToVideo):
	cmd = "ffprobe.exe -v quiet -print_format json -show_streams -show_format"
	args = shlex.split(cmd)
	args.append(pathToVideo)
	# run the ffprobe process, decode stdout into utf-a and convert to JSON
	ffprobeOutput = subprocess.check_output(args).decode('utf-8')
	ffprobeOutput = json.loads(ffprobeOutput)
	#jsonList.append(ffprobeOutput)
	return ffprobeOutput

fileList = getListOfFiles(path)
filteredFileList = filterList(fileList)
jsonList.append(getVideoMetadata(filteredFileList[0]))
#print(jsonList[0])

if True:
	for i in filteredFileList:
		print (i)
		# If wanted to print each line by line
		print ()