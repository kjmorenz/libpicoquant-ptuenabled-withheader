


from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import os

class Curve:
    filetype = 'PHU'                    
    FileCreated = -1
    Measurement_Mode = -1
    NumberOfCurves = -1
    BitsPerBin = -1
    BinningFactor = -1
    AcqTime = -1
    TimeLog = ""
    TimeFrom = -1
    TimeTo = -1
    CountFrom = -1
    CountTo = -1
    BaseRes = -1
    InputChannels = -1
    ExternalRefClock = ""
    HWSyncDivider = -1
    SyncCFDLevel = -1
    SyncCFDZeroCross = -1
    SyncOffset = -1
    
    ChannelOneCFD = -1
    ChannelOneZeroCross = -1
    ChannelOneOffset = -1
    Chan1Enable = ""
    ChannelTwoCFD = -1
    ChannelTwoZeroCross = -1
    ChannelTwoOffset = -1
    Chan2Enable = ""

    ResUsed = -1
    NumBins = -1
    SyncRate = -1
    IntegralCount = -1
    

    counts = []             #

    textFileLine = ""       #
    sample = -1             #
    run = -1                #
    personName = ""         #
    date = -1               #
    emWavelength = -1       #
    material = ""           #
    solvent = ""            #
    filterWavelength = -1   #
    filterType = ""         #
    expwr = -1              #
    expwrunits = ""         #
    exWavelength = -1       #
    laserrep = -1           #
    det = ""                #
    filename = ""           #

    peak = -1

    
    #sample-run - person-date-somenumber-emwavelength-material=>solvent<filter>expwr-exwavelength-freqofsomekind(detectorID)
    def getTimeVector(self):
        time = []
        for i in range(self.NumBins):
            time.append(i*self.Res) # do I want Res or ResUsed?
            
        return time
    
    def fread(self, f, n, dtype): #f is file name, n is number of bits to read, dtype is data type
        """A clone of MATLAB's 'fread' function.  Numpy must be imported"""
        if dtype is np.str:
            dt=np.uint8
        else:
            dt=dtype

        data_array=np.fromfile(f, dt, n)
        #data_array.shape=(n,1)
        return data_array
    
    def __init__(self, txtFileLine,dataFolder):
        self.textFileLine = txtFileLine
        if len(self.textFileLine) > 65:#Parsing text file line
            self.sample = int(self.textFileLine[0:2])
            self.run = int(self.textFileLine[3:5])
            self.personName = self.textFileLine[8:14]
            self.date = int(self.textFileLine[14:20])
            self.expwr = int(self.textFileLine[22:25])
            self.expwrunits = self.textFileLine[25:27]
            self.exWavelength = int(self.textFileLine[27:31])
            self.laserrep = int(self.textFileLine[33:36])
            self.filterWavelength = int(self.textFileLine[40:44])
            self.filterType = self.textFileLine[46:48]
            self.emWavelength = int(self.textFileLine[49:53])
            self.det = self.textFileLine[56:64]

            self.filetype = self.textFileLine[-3:len(self.textFileLine)]
            
            index = 66
            nextChar = self.textFileLine[index]
            i = 0                
            while nextChar != '>':
                index = index+1
                self.material = self.material + nextChar
                nextChar = self.textFileLine[index]

            index = index+1
            nextChar = self.textFileLine[index]
            while nextChar != '-':
                index = index+1
                self.solvent = self.solvent + nextChar
                nextChar = self.textFileLine[index]

            index = index+1
            self.filename = self.textFileLine[index:len(self.textFileLine)]

            if self.filetype == 'phu':
                os.chdir(dataFolder)
                f = open(self.filename, 'rb')
                
                #Constants
                tyEmpty8      = int('FFFF0008',16)
                tyBool8       = int('00000008',16)
                tyInt8        = int('10000008',16)
                tyBitSet64    = int('11000008',16)
                tyColor8      = int('12000008',16)
                tyFloat8      = int('20000008',16)
                tyTDateTime   = int('21000008',16)
                tyFloat8Array = int('2001FFFF',16)
                tyAnsiString  = int('4001FFFF',16)
                tyWideString  = int('4002FFFF',16)
                tyBinaryBlob  = int('FFFFFFFF',16)
                
                Magic=self.fread(f,8,'S1') #Magic is an array
                MGC=''
                for i in Magic:
                    MGC+=i.decode('UTF-8') #turn it into a string
                if MGC!="PQHISTO": #check we have a PHU file
                    raise LoadError('This is not a PHU file')
                Version=self.fread(f,8,"S1")
                ##VRSN=''
                ##for i in Version: #don't know what this version is
                ##    VRSN+=i
                emp={}#empty dictionary. emp because it's empty right now :/
                
                while 1:
                    TagIdentt=self.fread(f,32,'S1') #current header item being read --> read first 32 bits after current postion as string
                    TagIdx=int((self.fread(f,1,'int32'))) #curve tag is referring to is stored in file in weird way
                    TagTyp=int((self.fread(f,1,'uint32'))) #data type (as above)
                    TagIdent=''
                    for i in TagIdentt:
                        TagIdent+=i.decode('UTF-8') #to string
                    if TagIdent=='Header_End':
                        break
                    EvalName = TagIdent
                    if TagIdx>-1:
                        EvalName=EvalName+ '(' +str(TagIdx+1) + ')'#TagIdx corresponds to curve this tag is referring to
                    if TagTyp==tyEmpty8:
                        self.fread(f,1,'int64')
                        #print "<Empty>"
                    elif TagTyp==tyBool8:
                        TagInt=self.fread(f,1,'int64')
                        if TagInt==0:
                            #print "FALSE"
                            emp[EvalName]='False'
                        else:
                            #print "TRUE"
                            emp[EvalName]='True'
                    elif TagTyp==tyInt8:
                        TagInt=self.fread(f,1,'int64')
                        #print '%d' %TagInt
                        emp[EvalName]=TagInt
                    elif TagTyp==tyBitSet64:
                        TagInt=self.fread(f,1,'int64')
                        #print '%X' %TagInt
                        emp[EvalName]=TagInt
                    elif TagTyp==tyColor8:
                        TagInt=self.fread(f,1,'int64')
                        #print "%X" %TagInt
                        emp[EvalName]=TagInt
                    elif TagTyp==tyFloat8:
                        TagFloat=self.fread(f,1,'float64')
                        #print "%E" %TagFloat
                        emp[EvalName]=TagFloat
                    elif TagTyp==tyFloat8Array:
                        TagInt=self.fread(f,1,'int64')
                        #print ("Float array with %d entries" %(TagInt/8))
                    elif TagTyp==tyTDateTime:
                        TagFloat=self.fread(f,1,'float64')
                        #print ('%s' %TagFloat)
                        emp[EvalName]=TagFloat
                    elif TagTyp==tyAnsiString:
                        TagInt=self.fread(f,1,'int64')
                        TagString=self.fread(f,TagInt,"S1")
                        #print ("%s" %TagString)
                        if TagIdx>-1:
                            EvalName=TagIdent + '(' +str(TagIdx+1) + ',:)'
                        emp[EvalName]=TagString
                    elif TagTyp==tyWideString:
                        TagInt=self.fread(f,1,'int64')
                        TagString=self.fread(f,TagInt,"S1")
                        #print ("%s" %TagString)
                        if TagIdx>-1:
                            EvalName=TagIdent + '(' + str(TagIdx+1) + ',:)'
                        emp[EvalName]= TagString
                    elif TagTyp==tyBinaryBlob:
                        TagInt=self.fread(f,1,'int64')
                        #print ("Binary Blob with %d Bytes" %TagInt)

                self.FileCreated = np.asscalar(emp["File_CreatingTime"])
                self.Measurement_Mode = np.asscalar(emp["Measurement_Mode"])
                self.NumberOfCurves = np.asscalar(emp["HistoResult_NumberOfCurves"])
                self.BitsPerBin = np.asscalar(emp["HistoResult_BitsPerBin"])
                self.BinningFactor = np.asscalar(emp["MeasDesc_BinningFactor"])
                self.AcqTime = np.asscalar(emp["MeasDesc_AcquisitionTime"])
                self.TimeLog = "".join(emp["CurSWSetting_DispLog"])
                self.TimeFrom = np.asscalar(emp["CurSWSetting_DispAxisTimeFrom"])
                self.TimeTo = np.asscalar(emp["CurSWSetting_DispAxisTimeTo"])
                self.CountFrom = np.asscalar(emp["CurSWSetting_DispAxisCountFrom"])
                self.CountTo = np.asscalar(emp["CurSWSetting_DispAxisCountTo"])
                self.BaseRes = np.asscalar(emp["HW_BaseResolution"])
                self.InputChannels = np.asscalar(emp["HW_InpChannels"])
                self.ExternalRefClock = "".join(emp["HW_ExternalRefClock"])
                self.HWSyncDivider = np.asscalar(emp["HWSync_Divider"])
                self.SyncCFDLevel = np.asscalar(emp["HWSync_CFDLevel"])
                self.SyncCFDZeroCross = np.asscalar(emp["HWSync_CFDZeroCross"])
                self.SyncOffset = np.asscalar(emp["HWSync_Offset"])

                self.ChannelOneCFD = np.asscalar(emp["HWInpChan_CFDLevel(1)"])
                self.ChannelOneZeroCross = np.asscalar(emp["HWInpChan_CFDZeroCross(1)"])
                self.ChannelOneOffset = np.asscalar(emp["HWInpChan_Offset(1)"])
                self.Chan1Enable = "".join(emp["HWInpChan_Enabled(1)"])
                self.ChannelTwoCFD = np.asscalar(emp["HWInpChan_CFDLevel(2)"])
                self.ChannelTwoZeroCross = np.asscalar(emp["HWInpChan_CFDZeroCross(2)"])
                self.ChannelTwoOffset = np.asscalar(emp["HWInpChan_Offset(2)"])
                self.Chan2Enable = "".join(emp["HWInpChan_Enabled(2)"])


                #Curve/run specific stuff

                dictKey = str(self.run)
                    
                self.ResUsed = np.asscalar(emp["HistResDscr_MDescResolution(" + dictKey + ")"])
                self.NumBins = np.asscalar(emp["HistResDscr_HistogramBins(" + dictKey + ")"])
                self.SyncRate = np.asscalar(emp["HistResDscr_SyncRate(" + dictKey + ")"])
                self.IntegralCount = np.asscalar(emp["HistResDscr_IntegralCount(" + dictKey + ")"])
                self.CurveIndex = np.asscalar(emp["HistResDscr_CurveIndex(" + dictKey + ")"])
                  
                
                f.seek(emp["HistResDscr_DataOffset(" + dictKey + ")"],0)
                    
                self.counts = self.fread(f,emp["HistResDscr_HistogramBins(" + dictKey + ")"],'uint32')
                f.close()

                for i in self.counts:
                    if i > self.peak:
                        self.peak = i

#test dummies:
##newCurve = Curve("01-01 - XXXXXX000000ex333WW4444nm555kHz<6666nmYY>7777nm(DDDDDDDD)-sample name>solventname-2017-03-07 Marks CdSe Dots Ensemble.phu","C:/Users/Karen/Desktop/")
##
##
##
##plt.semilogy(newCurve.counts)
##plt.xlabel('Run ' + str(newCurve.run))
##plt.ylabel('Log(Counts)')
##plt.show()
##
##f.close()
