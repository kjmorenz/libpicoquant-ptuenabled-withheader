
'''This script parses .PTU files from the Time/Pico/Hydra-Harp series of TCSPC modules.

Issues:  All header info is read into a dict, so far cannot iteratively output values for certain parameters, e.g. Resolution on each channel still needs to be pulled manually,
this is because Python assigns values in dicts as strings, so for example HistResDscr_MDescResolution(1) must have the "1" inputted manually, instead of writing a for to output each one.
This will be fixed in v3.0'''

from matplotlib import pyplot as plt
from datetime import datetime
class LoadError(Exception):
    pass
import numpy as np
import os
FilePath=('C:/Users/Minhal/Desktop')
os.chdir(FilePath)
#Load file
f=open("2017-03-07 Mark's CdSe Dots Ensemble.phu",'rb')
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



Magic=fread(f,8,'S1')
MGC=''
for i in Magic:
    MGC+=i
if MGC!='PQHISTO':
    raise LoadError('This is not a PHU file')
Version=fread(f,8,"S1")
VRSN=''
for i in Version:
    VRSN+=i
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
FileCreated=np.asscalar(emp["File_CreatingTime"])
print ("File Created: %s" %(datetime.fromtimestamp(FileCreated).strftime('%Y-%m-%d')))
Measurement_Mode=np.asscalar(emp["Measurement_Mode"])
print ("Measurement Mode: %d" %Measurement_Mode)
NumberOfCurves=np.asscalar(emp["HistoResult_NumberOfCurves"])
print ("Number of Curves: %d" %NumberOfCurves)
BitsPerBin=np.asscalar(emp["HistoResult_BitsPerBin"])
print ("Bits per Bin: %d" %BitsPerBin)
BinningFactor=np.asscalar(emp["MeasDesc_BinningFactor"])
print ("Binning Factor: %d" %BinningFactor)
AcqTime=np.asscalar(emp["MeasDesc_AcquisitionTime"])
print ("Acquisition Time: %d" %AcqTime)
TimeLog="".join(emp["CurSWSetting_DispLog"])
print ("Log Time Axis?: %s" %TimeLog)
TimeFrom=np.asscalar(emp["CurSWSetting_DispAxisTimeFrom"])
print ("Display Time Axis From : %s" %TimeFrom)
TimeTo=np.asscalar(emp["CurSWSetting_DispAxisTimeTo"])
print ("Display Time Axis To : %s" %TimeTo)
CountFrom=np.asscalar(emp["CurSWSetting_DispAxisCountFrom"])
print ("Display Count Axis From: %s" %CountFrom)
CountTo=np.asscalar(emp["CurSWSetting_DispAxisCountTo"])
print ("Display Count Axis To: %s" %CountTo)
Res=np.asscalar(emp["HW_BaseResolution"])
print ("Hardware Base Resolution: %e (ps)" %Res)
InputChannels=np.asscalar(emp["HW_InpChannels"])
print ("Number of Input Channels: %d" %InputChannels)
ExternalRefClock="".join(emp["HW_ExternalRefClock"])
print ("External Reference Clock?: %s" %ExternalRefClock)
HWSyncDivider=np.asscalar(emp["HWSync_Divider"])
print ("Sync Divider: %d" %HWSyncDivider)
SyncCFDLevel=np.asscalar(emp["HWSync_CFDLevel"])
print ("Sync CFD Level: %d (mV)" %SyncCFDLevel)
SyncCFDZeroCross=np.asscalar(emp["HWSync_CFDZeroCross"])
print ("Sync CFD Zero Cross: %d (mV)" %SyncCFDZeroCross)
SyncOffset=np.asscalar(emp["HWSync_Offset"])
print ("Sync Offset: %d" %SyncOffset)
ChannelOneCFD=np.asscalar(emp["HWInpChan_CFDLevel(1)"])
print ("Channel 1 CFD Level: %d (mV)" %ChannelOneCFD)
ChannelOneZeroCross=np.asscalar(emp["HWInpChan_CFDZeroCross(1)"])
print ("Channel 1 Zero Cross: %d (mV)" %ChannelOneZeroCross)
ChannelOneOffset=np.asscalar(emp["HWInpChan_Offset(1)"])
print ("Channel 1 Offset: %d" %ChannelOneOffset)
Chan1Enable="".join(emp["HWInpChan_Enabled(1)"])
print ("Channel 1 Enabled?: %s" %Chan1Enable)
ChannelTwoCFD=np.asscalar(emp["HWInpChan_CFDLevel(2)"])
print ("Channel 2 CFD Level: %d (mV)" %ChannelTwoCFD)
ChannelTwoZeroCross=np.asscalar(emp["HWInpChan_CFDZeroCross(2)"])
print ("Channel 2 Zero Cross: %d (mV)" %ChannelTwoZeroCross)
ChannelTwoOffset=np.asscalar(emp["HWInpChan_Offset(2)"])
print ("Channel 2 Offset: %d" %ChannelTwoOffset)
Chan2Enable="".join(emp["HWInpChan_Enabled(2)"])
print ("Channel 2 Enabled?: %s" %Chan2Enable)
ResUsed=np.asscalar(emp["HistResDscr_MDescResolution(1)"])
print ("Resolution used: %e (s)" %ResUsed) 
NumBins=np.asscalar(emp["HistResDscr_HistogramBins(1)"])
print ("Number of Bins: %s" %NumBins)
SyncRate=np.asscalar(emp["HistResDscr_SyncRate(1)"])
print ("Sync Rate: %s" %SyncRate)
IntegralCountChanOne=np.asscalar(emp["HistResDscr_IntegralCount(1)"])
print ("Channel 1 Total Counts: %d" %IntegralCountChanOne)
IntegralCountChanTwo=np.asscalar(emp["HistResDscr_IntegralCount(2)"])
print ("Channel 2 Total Counts: %d" %IntegralCountChanTwo)

#######################################################################
'''The following is super ugly and should by no means be taken as canon.
It just works.'''
'''Always call len(CountsN) and ensure the length is equal to number of bins'''
'''Find Method to iteratively output these values'''
'''f.seek(emp["HistResDscr_DataOffset(1)"],0)
Counts1=fread(f,emp["HistResDscr_HistogramBins(1)"],'uint32')
#print Counts1
Peak1=max(Counts1)
f.seek(emp["HistResDscr_DataOffset(2)"],0)
Counts2=fread(f,emp["HistResDscr_HistogramBins(2)"],'uint32')
Peak2=max(Counts2)
#print Counts2'''
Counts=[]
dictKey = "HistResDscr_HistogramBins("
for i in range(int(NumberOfCurves-1)+1):
    dictKey = dictKey + str(i) + ")"
    f.seek(emp[dictKey],0)
    Counts[i] = fread(f,emp[dictKey],'uint32')
    dictKey = "HistResDscr_HistogramBins("


########################################################################
print ("Curve Index: %d" %np.asscalar(emp["HistResDscr_CurveIndex(1)"]))
print ("Resolution: %e" %np.asscalar(emp["HistResDscr_MDescResolution(1)"]))
print ("Number Of Bins: %d" %np.asscalar(emp["HistResDscr_HistogramBins(1)"],))
print ("Peak Count: %d" %(Peak1))
print ("Total Count: %d" %np.asscalar(emp["HistResDscr_IntegralCount(1)"]))
print "####################################################################"
print ("Curve Index: %d" %np.asscalar(emp["HistResDscr_CurveIndex(2)"]))
print ("Resolution: %e" %np.asscalar(emp["HistResDscr_MDescResolution(2)"]))
print ("Number Of Bins: %d" %np.asscalar(emp["HistResDscr_HistogramBins(2)"],))
print ("Peak Count: %d" %(Peak2))
print ("Total Count: %d" %np.asscalar(emp["HistResDscr_IntegralCount(2)"]))

############################################################################
'''Again, ugly plotting routine but it works for now to generate
a histogram of the data.  The x-axis is just the index of CountsN'''
empty=[]
for i in range(len(Counts1)):
    empty.append(i)
plt.semilogy(empty,Counts1)
plt.xlabel('Channel 1')
plt.ylabel('Log(Counts)')
plt.show()

f.close()
