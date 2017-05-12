
from matplotlib import pyplot as plt
from datetime import datetime
class LoadError(Exception):
    pass
import numpy as np
import os
FilePath=('C:/Users/Minhal/Desktop/')
os.chdir(FilePath)
#Load file
global f
f=open("2017-04-18 Mark Dots in SolutionMediumExcitationIntensity T2 30.ptu",'rb')
def fread(f, n, dtype):
    """A clone of MATLAB's 'fread' function.  Numpy must be imported"""
    if dtype is np.str:
        dt=np.uint8
    else:
        dt=dtype

    data_array=np.fromfile(f, dt, n)
    #data_array.shape=(n,1)
    return data_array


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


#Globals for subroutines
global TTResultFormat_TTTRRecType
global TTResult_NumberOfRecords
global MeasDesc_Resolution
global MeasDesc_GlobalResolution

TTResultFormat_TTTRRecType = 0
TTResult_NumberOfRecords = 0
MeasDesc_Resolution = 0
MeasDesc_GlobalResolution = 0



#Make sure it's a PTU file
Magic=fread(f,8,'S1')
MGC=''
for i in Magic:
    MGC+=i
if MGC!='PQTTTR':
    raise LoadError('This is not a PTU file')


#Version check
Version=fread(f,8,"S1")
VRSN=''
for i in Version:
    VRSN+=i

#Read header
#There's no do...while so instead while True if (expr) break
emp={}
while 1:
    TagIdentt=fread(f,32,'S1')
    TagIdx=int((fread(f,1,'int32')))
    TagTyp=int((fread(f,1,'uint32')))
    TagIdent=''
    for i in TagIdentt:
        TagIdent+=i
    if TagIdx>-1:
        EvalName=TagIdent+ '(' +str(TagIdx+1) + ')'
    else:
        EvalName=TagIdent
    if TagTyp==tyEmpty8:
        fread(f,1,'int64')
        #print "<Empty>"
    elif TagTyp==tyBool8:
        TagInt=fread(f,1,'int64')
        if TagInt==0:
            #print "FALSE"
            emp[EvalName]='False'
        else:
            #print "TRUE"
            emp[EvalName]='True'
    elif TagTyp==tyInt8:
        TagInt=fread(f,1,'int64')
        #print '%d' %TagInt
        emp[EvalName]=TagInt
    elif TagTyp==tyBitSet64:
        TagInt==fread(f,1,'int64')
        #print '%X' %TagInt
        emp[EvalName]=TagInt
    elif TagTyp==tyColor8:
        TagInt=fread(f,1,'int64')
        #print "%X" %TagInt
        emp[EvalName]=TagInt
    elif TagTyp==tyFloat8:
        TagFloat=fread(f,1,'float64')
        #print "%E" %TagFloat
        emp[EvalName]=TagFloat
    elif TagTyp==tyFloat8Array:
        TagInt=fread(f,1,'int64')
        #print ("Float array with %d entries" %(TagInt/8))
    elif TagTyp==tyTDateTime:
        TagFloat=fread(f,1,'float64')
        #print ('%s' %TagFloat)
        emp[EvalName]=TagFloat
    elif TagTyp==tyAnsiString:
        TagInt=fread(f,1,'int64')
        TagString=fread(f,TagInt,"S1")
        #print ("%s" %TagString)
        emp[EvalName]=TagString
        if TagIdx>-1:
            EvalName=TagIdent + '(' +str(TagIdx+1) + ',:)'
    elif TagTyp==tyWideString:
        TagInt=fread(f,1,'int64')
        TagString=fread(f,TagInt,"S1")
        #print ("%s" %TagString)
        if TagIdx>-1:
            EvalName=TagIdent + '(' + str(TagIdx+1) + ',:)'
        emp[EvalName]= TagString
    elif TagTyp==tyBinaryBlob:
        TagInt=fread(f,1,'int64')
        #print ("Binary Blob with %d Bytes" %TagInt)
    if TagIdent=='Header_End':
        break
#####################################################################
#File object to write T2/T3 data in ASCII
#File will by default be outputted as .txt
#This is not to be used and thus will be commented out
#The write will take a very long time and likely consume exorbitant amounts of disk space
#global fpout
#fpout=open('2017-04-18 Mark Dots in SolutionMediumExcitationIntensity T2 30.ptu.txt','w')














################################################################
#Clean up dtypes for some parameters
TTResultFormat_TTTRRecType = int(np.asscalar(emp["TTResultFormat_TTTRRecType"]))
TTResult_NumberOfRecords = int(np.asscalar(emp["TTResult_NumberOfRecords"]))
MeasDesc_Resolution = (np.asscalar(emp["MeasDesc_Resolution"]))
MeasDesc_GlobalResolution = (np.asscalar(emp["MeasDesc_GlobalResolution"]))
################################################################


################################################################
#Check the type of record we have
global isT2
isT2=0
if np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtPicoHarpT3:
    isT2=False
    print ("PicoHarp T3 Data")
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtPicoHarpT2:
    isT2=True
    print ("PicoHarp T2 Data")
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarpT3:
    isT2=False
    print ("HydraHarp V1 T3 Data")
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarpT2:
    isT2=True
    print ("HydraHarp V1 T2 Data")
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarp2T3:
    isT2=False
    print ("PicoHarp V2 T3 Data")
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtHydraHarp2T2:
    isT2=True
    print ("HydraHarp V2 T2 Data")
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtTimeHarp260NT3:
    isT2 = False
    print ('TimeHarp260N T3 data')
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtTimeHarp260NT2:
    isT2 = True
    print ('TimeHarp260N T2 data')
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])== rtTimeHarp260PT3:
    isT2 = False
    print('TimeHarp260P T3 data')
elif np.asscalar(emp["TTResultFormat_TTTRRecType"])==rtTimeHarp260PT2:
    isT2 = True
    print('TimeHarp260P T2 data')
else:
    print ('Illegal Record Type')
###########################################################################

#Nice functions for nice people
def GotPhoton(TimeTag,Channel,DTime):
    global isT2
    global RecNum
    global MeasDesc_GlobalResolution
    global cnt_ph
    cnt_ph =1
    if isT2:
        print(RecNum, np.asscalar(Channel), np.asscalar(TimeTag),np.asscalar((TimeTag * MeasDesc_GlobalResolution * 1e12)))
    else:
        print(RecNum, np.asscalar(Channel), np.asscalar(TimeTag), np.asscalar((TimeTag * MeasDesc_GlobalResolution * 1e9)),DTime)
def GotMarker(TimeTag,Markers):
    global RecNum
    global cnt_ma
    cnt_ma=1
    print (RecNum, np.asscalar(Markers), np.asscalar(TimeTag))
def GotOverflow(Count):
    global RecNum
    global cnt_ov
    cnt_ov=Count
    print (RecNum, np.asscalar(Count))
#####################################################################

#Decoder Functions
#Reads T2 Data (HydraHarp ONLY)
def ReadHT2(Version):
    global f
    global TTResult_NumberOfRecords
    global RecNum
    OverflowCorrection=0
    T2WRAPAROUND_V1=33552000
    T2WRAPAROUND_V2=33554432

    for i in range(TTResult_NumberOfRecords):
        RecNum=i
        T2Record=fread(f,1,'uint32')
        dtime=T2Record&33554431
        channel=(T2Record>>25)&63
        special=(T2Record>>31)&1
        timetag=OverflowCorrection+dtime
        if special==0:
            GotPhoton(timetag, channel+1,0)
        else:
            if channel==63:
                if Version==1:
                    OverflowCorrection=OverflowCorrection+T2WRAPAROUND_V1
                    GotOverflow(1)
                else:
                    if dtime==0:
                        OverflowCorrection=OverflowCorrection+T2WRAPAROUND_V2
                        GotOverflow(1)
                    else:
                        OverflowCorrection = OverflowCorrection + T2WRAPAROUND_V2 * dtime
                        GotOverflow(dtime)
            if channel==0:
                GotPhoton(timetag,channel,0)
            if channel>=1 and channel<=15:
                GotMarker(timetag,channel)
        
#Reads T3 Data (HydraHarp ONLY)
def ReadHT3(Version):
    global f
    global RecNum
    global TTResult_NumberOfRecords
    OverflowCorrection=0
    T3WRAPAROUND=1024

    for i in range(TTResult_NumberOfRecords):
        RecNum=i
        T3Record=fread(f,1,'uint32')
        nsync=T3Record&1023
        dtime=(T3Record>>10)&32767
        channel=(T3Record>>25)&63
        special=(T3Record>>31)&1

        if special==0:
            true_nSync=OverflowCorrection+nsync
            GotPhoton(true_nSync, channel, dtime)
        else:
            if channel==63:
                if nsync==0 or Version==1:
                    OverflowCorrection=OverflowCorrection+T3WRAPAROUND
                    GotOverflow(1)
                else:
                    OverflowCorrection=OverflowCorrection+T3WRAPAROUND*nsync
                    GotOverflow(nsync)
            if (channel>=1) and (channel<=15):
                true_nSync=OverflowCorrection+nsync
                GotMarker(true_nSync,channel)
