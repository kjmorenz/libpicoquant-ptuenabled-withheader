import os
import re
import numpy as np
class CustomError(Exception):
    pass

def regexp(folder, filenames):
    newlist = []
    
    header = re.compile('\d\d-\d\d\s-\s')

    for item in filenames:
        filename = folder + item 
        file = open(filename)
        for line in file.readlines():
            if header.match(line) != None:
                newlist.append(line[:len(line)-1])
        file.close()

    return newlist

PathD="C:\\Users\\Karen\\Dropbox (WilsonLab)\\WilsonLab Team Folder\\Programs\\2016-12-21 - Mark's Matlab Data Analysis Package\\test data\\"
Files=os.listdir(PathD)
os.chdir(PathD)

ndf=0
FileList=[] #datafiles
for i in range(len(Files)):
    if len(Files[i])>=8 and Files[i][-8:] == 'Data.phd':
        ndf+=1
    if Files[i][-8:]=='Data.phd':
        FileList.append(Files[i])
               
if ndf==0:
    print("No .phd files detected")

NumTitleFiles=0
TitleList=[] #log files
for i in range(len(Files)):
    if len(Files[i])>=20 and Files[i][-20:]=='Experimental Log.txt':
        NumTitleFiles+=1
    if Files[i][-20:]=='Experimental Log.txt':
        TitleList.append(Files[i])
        
if NumTitleFiles==0:
    print('Warning: Could not detect any files in the form ***Experimental Log.txt***')
    print('At present, this is required for program execution, program will now terminate')
    raise CustomError('Unable to generate LegendHeaders')

if len(TitleList)!=len(FileList):
    print('Warning: This folder contains a different number of Data and Experimental Log files')
    dummy=input('Press <Enter> to Continue, or Ctrl-C to quit')
    print('Continuing Program Execution')

#fid=[]
#fid=[open(i).readlines() for i in TitleList]
#print fid

logDetails = regexp(PathD, TitleList)
#print ndf,FileList,NumTitleFiles,TitleList
