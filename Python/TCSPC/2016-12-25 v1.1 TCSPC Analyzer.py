#Code to Analyze TCSPC Data#
import os as os ###For all the operating system interactions (Automatic in MATLAB)###
import re
import numpy as np
from matplotlib import pyplot as plt
import warnings
from curve import Curve
from clearvars import clearvars
from regexp import regexp
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

PathD='C:/Users/Karen/Desktop/'  ###Note: Don't use double \\ when declaring path###
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
##import Tkinter as tk
##root=tk.Tk()
##screenwidth=root.winfo_screenwidth()
##screenheight=root.winfo_screenheight() 
##dim_screen=[screenwidth, screenheight]  ###Put it into a list###
##DefaultFigPosition=[dim_screen[0]-DefaultFigSize[0],dim_screen[1]-DefaultFigSize[1]]
##if min(DefaultFigPosition)<=0:
##  raise CustomError('Current display resolution too small to display standard figure')
###DefaultFigPosition is a list, if either dimension is less than
###zero, raises error.
  
sumClr = sum(DefaultFigColour)
if sumClr==3 and not os.path.exists('Analysis\White'):
  os.makedirs('Analysis\White')
elif sumClr==0 and not os.path.exists('Analysis\Black'):
  os.makedirs('Analysis\Black')
elif sumClr != 3 and sumClr != 0:
  raise CustomError('DefaultFigColour is neither white nor black -- this case is not yet supported by the program, please retry')

#warnings.warn('NegativeDataIgnored')  Re-enable this at the end

##LOAD DATA##

if "MainData" in globals():
    LoadSkip=True
    print("**********************************************************")
    print("Data Detected in Memory - Skipping Data Load")
    print("**********************************************************")
    dummy=raw_input('Press <Enter> to continue')
    print("Continuing program execution...")
    del dummy
else:
    LoadSkip=False
    print("**********************************************************")
    print("No Data Detected in Memory")
    print("--> Proceeding to Load Data...")
    print("**********************************************************")

##Clear Memory  
if LoadSkip==False:
    skipvars = ['var', 'skipvars', 'delnames',  'LoadSkip',
                'DoParam', 'PathD', 'ResetPlot', 'DefaultFigSize',
                'DefaultFigColour', 'DefaultFigPosn', 'isSaveFigs',
                'os', 'plt', 're','np','warnings','Curve','CustomError',
                'regexp', 'clearvars']
    clearvars(skipvars)
    print("Loading data...")
    Files=[f for f in os.listdir('.') if os.path.isfile(f)]
    print("Loading .txt log files files...")
    print('Generating LegendHeaders from *Experimental Log.txt')
    ExpLogFiles = []
    for i in range(len(Files)):
        if len(Files[i])>=20 and Files[i][-20:]=='Experimental Log.txt':
            ExpLogFiles.append(Files[i])
    if ExpLogFiles==[]:
        print('Warning: Could not detect any files in the form ***...Experimental Log.txt***')
        print('At present, this is required for program execution, program will now terminate')
        raise CustomError('Unable to generate LegendHeaders')
    else:
        logDetails = regexp(PathD, ExpLogFiles)
  




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
        #ColourSet[j]=
        donothing=j



  
  
  
