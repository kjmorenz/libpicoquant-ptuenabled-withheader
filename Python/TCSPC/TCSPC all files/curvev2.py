


from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import os

class Curve:
    #for all 
    filetype = ''
    MGC=''
    VRSN=''
    FileCreated = -1
    Measurement_Mode = -1
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

    SyncRate = -1

##  PHU specific    
    NumberOfCurves = -1
    BitsPerBin = -1

##  PHU curve specific
    ResUsed = -1
    NumBins = -1
    IntegralCount = -1
    CurveIndex = -1

##  PTU specific
    HydraHarpVersion = 2 #Change this if you have a different version of the HydraHarp!
    
    isT2 = None
    isT2tag = ''
    

    StopReason = -1
    TTResultFormat_TTTRRecType = 0
    TTResultFormat_BitsPerRecord = 0
    Offset = 0
    StopAt = 0
    StopOnOvfl = None
    Restart = None
    MeasDesc_Resolution = 0
    HW_Markers = 0
    MeasDesc_GlobalResolution = 0
    InputRate0 = 0
    InputRate1 = 0
    StopAfter = 0
    NumberOfRecords = 0

    
##  PHU Data
    counts = []             #

##  Experimental Log Text File data
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

    def GotPhoton(self, RecNum, TimeTag,Channel,DTime):
        if self.isT2:
            return ['P', RecNum, np.asscalar(Channel), np.asscalar(TimeTag),np.asscalar((TimeTag * self.MeasDesc_GlobalResolution
                                                                                  * 1e12))]
        else:
            return ['P', RecNum, np.asscalar(Channel), np.asscalar(TimeTag), np.asscalar((TimeTag * self.MeasDesc_GlobalResolution
                                                                            * 1e9)),np.asscalar(DTime))
    def GotMarker(self, RecNum, TimeTag,Markers):
        return ['M', RecNum, np.asscalar(Markers), np.asscalar(TimeTag)]

    def GotOverflow(self, RecNum, dtime):
        return ['O', RecNum, np.asscalar(dtime)]

    def ReadHT2(self,ReadFrom, ReadTo):
        f = open(self.filename, 'rb')
        OverflowCorrection=0 #need to fix overflow correction - it needs to know about everything previous!!!
        T2WRAPAROUND_V1=33552000
        T2WRAPAROUND_V2=33554432
        
##      Note that the raw data is time ordered
        rval = []
        for i in range(ReadTo):#for overflow correction need to read from 0 - it needs to know about everything previous!!!
            T2Record=self.fread(f,1,'uint32')
            dtime=T2Record&33554431 ## & does a bitwise output: each bit of the output is 1 iff the corresponding bit of x and y is 1, otherwise it's 0
            channel=(T2Record>>25)&63
            special=(T2Record>>31)&1
             
            if special==0 and i >= ReadFrom::
                rval.append(self.GotPhoton(i+ReadFrom,timetag, channel+1,0))
            else:
                if channel==63:
                    if self.HydraHarpVersion==1:
                        OverflowCorrection=OverflowCorrection+T2WRAPAROUND_V1
                        if i >= ReadFrom:
                            rval.append(self.GotOverflow(i+ReadFrom,1))#why is this 1 and not dtime?
                    else:
                        if dtime==0:
                            OverflowCorrection=OverflowCorrection+T2WRAPAROUND_V2
                            if i >= ReadFrom:
                                rval.append(self.GotOverflow(i+ReadFrom,1))
                        else:
                            OverflowCorrection = OverflowCorrection + T2WRAPAROUND_V2 * dtime
                            if i >= ReadFrom:
                                rval.append(self.GotOverflow(i+ReadFrom,dtime))
                if channel==0 and i >= ReadFrom::
                    rval.append(self.GotPhoton(i+ReadFrom, timetag,channel,0))
                if channel>=1 and channel<=15 and i >= ReadFrom::
                    rval.append(self.GotMarker(i+ReadFrom, timetag,channel))
        f.close()
        return rval

    def ReadHT3(self,ReadFrom, ReadTo):
        f = open(self.filename, 'rb')
        OverflowCorrection=0 
        T3WRAPAROUND=1024

        rval = []
        for i in range(ReadTo):#for overflow correction need to read from 0 - it needs to know about everything previous!!!
            T3Record=fread(f,1,'uint32')
            nsync=T3Record&1023
            dtime=(T3Record>>10)&32767
            channel=(T3Record>>25)&63
            special=(T3Record>>31)&1

            if special==0:
                true_nSync=OverflowCorrection+nsync
                if i >= ReadFrom:
                    rval.append(self.GotPhoton(i+ReadFrom,true_nSync, channel, dtime))
            else:
                if channel==63:
                    if nsync==0 or Version==1:
                        OverflowCorrection=OverflowCorrection+T3WRAPAROUND
                        if i >= ReadFrom:
                            rval.append(self.GotOverflow(i+ReadFrom,1))
                    else:
                        OverflowCorrection=OverflowCorrection+T3WRAPAROUND*nsync
                        if i >= ReadFrom:
                            rval.append(self.GotOverflow(i+ReadFrom,nsync))
                if (channel>=1) and (channel<=15):
                    true_nSync=OverflowCorrection+nsync
                    if i >= ReadFrom:
                        rval.append(self.GotMarker(i+ReadFrom,true_nSync,channel))
                    
        return rval
                
    def readTTdata(self, ReadFrom, ReadTo):
        if ReadFrom < 0:
            ReadFrom = 0
        if ReadTo < 0:
            return 'ReadTo < 0'
        if ReadFrom >= self.NumberOfRecords:
            return None
        if ReadTo > self.NumberOfRecords:
            ReadTo = self.NumberOfRecords
        if self.isT2 and self.isT2tag != 'Illegal Record Type':
            return self.ReadHT2(ReadFrom, ReadTo)
        elif not self.isT2 and self.isT2tag != 'Illegal Record Type':
            return self.ReadHT3(ReadFrom, ReadTo)
        else:
            return 'Illegal Record Type'
    
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

            if self.filetype != 'phu' or self.filetype != 'ptu':
                raise LoadError('This is not a PHU or PTU file')
            
            else:
                os.chdir(dataFolder)
                if self.filename
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
                
                for i in Magic:
                    self.MGC+=i.decode('UTF-8') #turn it into a string
                    
                if self.filetype == 'phu' and self.MGC!="PQHISTO": #check we have a PHU file
                    raise LoadError('This is not a PHU file')
                if self.filetype == 'ptu' and self.MGC!='PQTTTR':
                    raise LoadError('This is not a PTU file')
                    
                
                Version=self.fread(f,8,"S1")
                
                for i in Version: 
                    self.VRSN+=i
                        
                
                    
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
                self.ChannelOneCFD = np.asscalar(emp["HWInpChan_CFDLevel(0)"])
                self.ChannelOneZeroCross = np.asscalar(emp["HWInpChan_CFDZeroCross(0)"])
                self.ChannelOneOffset = np.asscalar(emp["HWInpChan_Offset(0)"])
                self.Chan1Enable = "".join(emp["HWInpChan_Enabled(0)"])
                self.ChannelTwoCFD = np.asscalar(emp["HWInpChan_CFDLevel(1)"])
                self.ChannelTwoZeroCross = np.asscalar(emp["HWInpChan_CFDZeroCross(1)"])
                self.ChannelTwoOffset = np.asscalar(emp["HWInpChan_Offset(1)"])
                self.Chan2Enable = "".join(emp["HWInpChan_Enabled(1)"])
                    
                if filetype == 'phu':
                    self.NumberOfCurves = np.asscalar(emp["HistoResult_NumberOfCurves"])#
                    self.BitsPerBin = np.asscalar(emp["HistoResult_BitsPerBin"])
                    
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

                elif self.filetype = 'ptu':

                    #These might be T2 specific too?
                    self.StopReason = np.asscalar(emp["TTResult_StopReason"])#
                    self.TTResultFormat_TTTRRecType = np.asscalar(emp["TTResultFormat_TTTRRecType"])
                    self.TTResultFormat_BitsPerRecord = np.asscalar(emp["TTResultFormat_BitsPerRecord"])
                    self.Offset = np.asscalar(emp["MeasDesc_Offset"])
                    self.StopAt = np.asscalar(emp["MeasDesc_StopAt"])
                    self.StopOnOvfl = np.asscalar(emp["MeasDesc_StopOnOvfl"])
                    self.Restart = np.asscalar(emp["MeasDesc_Restart"])
                    self.MeasDesc_Resolution = np.asscalar(emp["MeasDesc_Resolution"])
                    self.HW_Markers = np.asscalar(emp["HW_Markers"])
                    self.MeasDesc_GlobalResolution = np.asscalar(emp["MeasDesc_GlobalResolution"])
                    self.SyncRate = np.asscalar(emp["TTResult_SyncRate"])
                    self.InputRate0 = np.asscalar(emp["TTResult_InputRate(0)"])
                    self.InputRate1 = np.asscalar(emp["TTResult_InputRate(1)"])
                    self.StopAfter = np.asscalar(emp["TTResult_StopAfter"])
                    self.NumberOfRecords = np.asscalar(emp["TTResult_NumberOfRecords"])                   

                    
                    
                    #RecordTypes
                    rtPicoHarpT3     = int('00010303',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $03 (PicoHarp)
                    rtPicoHarpT2     = int('00010203',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $03 (PicoHarp)
                    rtHydraHarpT3    = int('00010304',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $04 (HydraHarp)
                    rtHydraHarpT2    = int('00010204',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $04 (HydraHarp)
                    rtHydraHarp2T3   = int('01010304',16)# (SubID = $01 ,RecFmt: $01) (V2), T-Mode: $03 (T3), HW: $04 (HydraHarp)
                    rtHydraHarp2T2   = int('01010204',16)# (SubID = $01 ,RecFmt: $01) (V2), T-Mode: $02 (T2), HW: $04 (HydraHarp)
                    rtTimeHarp260NT3 = int('00010305',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $05 (TimeHarp260N)
                    rtTimeHarp260NT2 = int('00010205',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $05 (TimeHarp260N)
                    rtTimeHarp260PT3 = int('00010306',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $03 (T3), HW: $06 (TimeHarp260P)
                    rtTimeHarp260PT2 = int('00010206',16)# (SubID = $00 ,RecFmt: $01) (V1), T-Mode: $02 (T2), HW: $06 (TimeHarp260P)

                    #Set isT2 and isT2tag - the data type
                            
                    if np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtPicoHarpT3:
                        self.isT2=False
                        self.isT2tag = "PicoHarp T3 Data"
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtPicoHarpT2:
                        self.isT2=True
                        self.isT2tag = "PicoHarp T2 Data"
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarpT3:
                        self.isT2=False
                        self.isT2tag = "HydraHarp V1 T3 Data"
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarpT2:
                        self.isT2=True
                        self.isT2tag = "HydraHarp V1 T2 Data"
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarp2T3:
                        self.isT2=False
                        self.isT2tag = "PicoHarp V2 T3 Data"
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarp2T2:
                        self.isT2=True
                        self.isT2tag = "HydraHarp V2 T2 Data"
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtTimeHarp260NT3:
                        self.isT2 = False
                        self.isT2tag = 'TimeHarp260N T3 data'
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtTimeHarp260NT2:
                        self.isT2 = True
                        self.isT2tag = 'TimeHarp260N T2 data'
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])== rtTimeHarp260PT3:
                        self.isT2 = False
                        self.isT2tag = 'TimeHarp260P T3 data'
                    elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtTimeHarp260PT2:
                        self.isT2 = True
                        self.isT2tag = 'TimeHarp260P T2 data'
                    else:
                        self.isT2tag = 'Illegal Record Type'
                        raise LoadError('Illegal Record Type - neither T2 nor T3')

                    f.close()
                        

                    

                    

                


                

                

                    

                    
                    
                

#test dummies:
##newCurve = Curve("01-01 - XXXXXX000000ex333WW4444nm555kHz<6666nmYY>7777nm(DDDDDDDD)-sample name>solventname-2017-03-07 Marks CdSe Dots Ensemble.phu","C:/Users/Karen/Desktop/")
##newCurve2 = Curve("01-02 - XXXXXX000000ex333WW4444nm555kHz<6666nmYY>7777nm(DDDDDDDD)-sample name>solventname-2017-03-07 Marks CdSe Dots Ensemble.phu","C:/Users/Karen/Desktop/")
##
##
##
##plt.semilogy(newCurve2.counts)
##plt.xlabel('Run ' + str(newCurve.run))
##plt.ylabel('Log(Counts)')
##plt.show()
##
##f.close()
