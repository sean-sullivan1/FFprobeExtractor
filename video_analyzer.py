import os
import subprocess
import shlex
import json

'''
For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):
	# create a list of file and sub directories 
	# names in the given directory 
	listOfFile = os.listdir(dirName)
	allFiles = list()
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

def findVideoMetadata(pathToInputVideo):
	cmd = "ffprobe.exe -v quiet -print_format json -show_streams -show_format"
	args = shlex.split(cmd)
	args.append(pathToInputVideo)
	# run the ffprobe process, decode stdout into utf-a and convert to JSON
	ffprobeOutput = subprocess.check_output(args).decode('utf-8')
	ffprobeOutput = json.loads(ffprobeOutput)
	jsonList.append(ffprobeOutput)

path = 'z:\\TV Shows\\'
fileList = getListOfFiles(path)
jsonList = list()

findVideoMetadata(fileList[3])
print(jsonList[0])

if 1 == 0:
	for i in fileList:
		print (i)
		# If wanted to print each line by line
		print ()