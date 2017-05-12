#Code to Analyze TCSPC Data#
import os  ###For all the operating system interactions (Automatic in MATLAB)###
import re
import numpy as np
import warnings
from curve.py import Curve
class CustomError(Exception):  ###Need this later for custom errors###
	pass

# User-set parameters for partial program execution - essentially, this is three programs in one
# '0' --> All subunits
# '1' --> Generate one plot with all raw curves from each .phu file
# '2' --> Generate one plot with all curves (background-subtracted & normalized) from each .phu file
# '3' --> Run the 'Good Bits' --> generally the user-specified 'particular plots'

DoParam=3   ###Make sure to check this flag

#User-set program execution parameters
#User-set flag to trigger export of .fig and .png files for each figure

isSaveFigs=False  ###Make sure to check this flag

#User-set home directory -- All .phu files in this directory will be loaded

PathD='C:\Users\...'  ###Note: Don't use double \\ when declaring path###
#PathD=PathD + ' \'   ###Actually don't need this as long as user is a useful user, leaving it for now###
os.chdir(PathD)       ###Might be a better way to do this, it just works###

# User-set parameter for figure background colour
# Note that setting this to black ([0 0 0]) or white ([1 1 1]) is used as a
# flag to control program execution to generate white- or black-background 
# figures -- other values are not yet handled.

DefaultFigColour=[1,1,1] ###Must pass a list###

#Setting this flag to 'False' tells the program not to alter the size/position of the figures

ResetPlot=False   ###How to do this in Python?##

#User-Set parameters for figure size
DefaultFigSize=[640,480]     
#Gets screen dimensions for figure sizing, not an array, just absolute dimensions
import Tkinter as tk
root=tk.Tk()
screenwidth=root.winfo_screenwidth()
screenheight=root.winfo_screenheight() 
dim_screen=[screenwidth, screenheight]  ###Put it into a list###
DefaultFigPosition=[dim_screen[0]-DefaultFigSize[0],dim_screen[1]-DefaultFigSize[1]]
if min(DefaultFigPosition)<=0:
	raise CustomError('Current display resolution too small to display standard figure')
###DefaultFigPosition is a list, if either dimension is less than
###zero, raises error.
	

if sum(DefaultFigColour)==3 and not os.path.exists('Analysis\White'):
	os.makedirs('Analysis\White')
elif sum(DefaultFigColour)==0 and not os.path.exists('Analysis\Black'):
	os.makedirs('Analysis\Black')
else:
	raise CustomError('DefaultFigColour is neither white nor black -- this case is not yet supported by the program, please retry')

#warnings.warn('NegativeDataIgnored')  Re-enable this at the end

##LOAD DATA##

if "MainData" in globals():  
    LoadSkip=True
    print "**********************************************************"
    print "Data Detected in Memory - Skipping Data Load"
    print "**********************************************************"
    dummy=raw_input('Press <Enter> to continue')
    print "Continuing program execution..."
    del dummy
else:
    LoadSkip=False
    print "**********************************************************"
    print "No Data Detected in Memory"
    print "--> Proceeding to Load Data..."
    print "**********************************************************"

##Clear Memory 	
if LoadSkip==False:		###Supposed to be for clearvars (line 110) but still need a clever way to 
    MainData=None               ###implement this in Python
    var = None
    delnames = []
    skipvars = ['var', 'skipvars', 'delnames',  'LoadSkip', 'DoParam', 'PathD', 'ResetPlot', 'DefaultFigSize', 'DefaultFigColour', 'DefaultFigPosn', 'isSaveFigs']
    for var in vars():
        if var not in skipvars and var[0] != '_':
            delnames.append(var)
    for i in range(len(delnames)):
	exec('del ' + delnames[i])
    del var
    del i

    #see clearvars snippet!

        
    ##clearvars -except LoadSkip DoParam PathD ResetPlot DefaultFigSize DefaultFigColour DefaultFigPosn isSaveFigs

'''	
if LoadSkip==False:
	MainData{1,1}.IsData=false ###Set flag to default
########NOT SURE WHAT IS GOING ON HERE, WHAT DOES THIS DO IN MATLAB
'''
    print "Loading data..."
    Files=os.listdir(PathD)
    print "Loading .phu files..."
	
	###Count number of valid files and build list of filenames###
	NumDataFiles=0
	for i in range(len(Files):
		if len(Files[i])>=8 and Files[i][-8:]=='Data.phu':   ###Ugly, but Pythonic 
			NumDataFiles+=1
		if Files[i][-8:]=='Data.phu':
        FileList.append(Files[i])
		elif:
			NumDataFiles=0
			print "No Data detected"
			
			for j in (0,NumDataFiles):
				MainData[j,1]=read_phd_mwbw.py(FileList[j]  
				#Probably need numpy array shaper
				MainData[j].Date=Filelist[j][1:10]
		
###Figure out the loading###


if LoadSkip=False or ##MainData{1,1}.IsData: #####Still don't know how to MainData###
	print 'Generating LegendHeaders from *Experimental Log.txt'
	
	####Count number of valid files and build list of filenames###
	NumTitleFiles=0
	TitleList=[]
	for i in range(len(Files)):
		if len(Files[i])>=20 and Files[i][-20:]=='Experimental Log.txt':
			NumTitleFiles+=1
		if Files[i][-20:]=='Experimental Log.txt':
			TitleList.append(Files[i])
        
	if NumTitleFiles==0:
		print 'Warning: Could not detect any files in the form ***Experimental Log.txt***'
		print 'At present, this is required for program execution, program will now terminate'
		raise CustomError('Unable to generate LegendHeaders')
		
	if len(TitleList)!=len(FileList):
		print 'Warning: This folder contains a different number of Data and Experimental Log files'
		dummy=raw_input('Press <Enter> to Continue, or Ctrl-C to quit')
		print 'Continuing Program Execution'
		
	#fid=[]  Potentially deprecated, will decide later 
	#fid=[open(i) for i in TitleList]  ###ListComp faster than for
	
	
def regexp(folder, filenames):
    newlist = []
    
    header = re.compile('\d\d-\d\d\s-\s')# this is the search key we'll look for at the start of lines

    for item in filenames:
        filename = folder + item 
        file = open(filename) # open the log file
        for line in file.readlines():
            if header.match(line) != None: #if the start of the line matches the search key
                newlist.append(line[:len(line)-1])#get rid of \n at end, add line to the list
        file.close()

    return newlist
logDetails = regexp(PathD, TitleList)


if DoParam==1 or DoParam==0 or DoParam==9:
	print('Plotting individual raw kinetics for .phu-style data...')
	if not MainData[1,1]==None:
		print('')
		print('DoParam has been set to:',DoParam, ', which plots .phu-style data')
		print('However, no.phu-style data is detected')
		print('Either change mode of operation (i.e. the value of DoParam)')
		print('...or ensure the .phu file(s) are in the directory specified in PathD')
		raise CustomError('No .phu-style data detected')
	for j in range(len(MainData)):
		ColourSet[j]=



	
	
	
