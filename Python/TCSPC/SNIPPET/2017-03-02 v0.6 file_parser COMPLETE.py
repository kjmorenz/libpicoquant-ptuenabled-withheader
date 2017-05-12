############################################################################
#This is a wrapper function that is to be used to parse binary file data from
#a .phd file.  It was ported over from MATLAB.  Please import NumPy or the script
#will not function correctly.  Feel free to comment out all the print statements
#they were only used to debug.
################################################################################
import os
from array import array  ###Don't suspect I need, but just in case
import numpy as np
os.chdir('C:\Users\Minhal\Desktop')
class CustomError(Exception):
    pass
 
def fread(f, n, dtype):
    """A clone of MATLAB's 'fread' function.  Numpy must be imported.
    f--> Filename (Including extension)
    n--> Number of BYTES to be read in
    dtype--> Data Type, as seen by NumPy, not Python default"""
    if dtype is np.str:
        dt=np.uint8
    else:
        dt=dtype
 
    data_array=np.fromfile(f, dt, n)
    #data_array.shape=(n,1)
    return data_array
 
f=open('2015-08-26-SWIRTCPSC-Data.phd','rb')
##############################################################
####################ASCII File Header#########################
##############################################################
Ident=fread(f,16,"S1")
IdentJ=''.join(Ident)
FormatVersion=fread(f, 6,"S1")
FVJ=''.join(FormatVersion)
if FVJ!='2.0':
   raise CustomError('Warning: This program is for version 2.0 only.  Aborted')
CreatorName=fread(f, 18, "S1")
CN=''.join(CreatorName)
CreatorVersion=fread(f,12,"S1")
CV=''.join(CreatorVersion)
FileTime=fread(f, 18, "S1")
FT=''.join(FileTime)
CRLF=fread(f,2,"S1")
clf=''.join(CRLF)
Comment=fread(f,256,"S1")
cm=''.join(Comment)
#############################################################
###################Binary File Header########################
#############################################################
NumberOfCurves=fread(f,1,"int32")
NOC=np.asscalar(NumberOfCurves)
BitsPerHistoBin=fread(f,1,'int32')
BPHB=np.asscalar(BitsPerHistoBin)
RoutingChannels=fread(f,1,'int32')
RC=np.asscalar(RoutingChannels)
NumberOfBoards=fread(f,1,'int32')
NOB=np.asscalar(NumberOfBoards)
ActiveCurve=fread(f,1,'int32')
AC=np.asscalar(ActiveCurve)
MeasurementMode=fread(f,1,'int32')
MM=np.asscalar(MeasurementMode)
SubMode=fread(f,1,'int32')
SM=np.asscalar(SubMode)
RangeNo=fread(f,1,'int32')
RN=np.asscalar(RangeNo)
Off_set=fread(f,1,'int32')
Offset=np.asscalar(Off_set)
AcquisitionTime=fread(f,1,'int32')
AcqT=np.asscalar(AcquisitionTime)
StopAt=fread(f,1,'int32')
SA=np.asscalar(StopAt)
StopOnOvfl=fread(f,1,'int32')
SOO=np.asscalar(StopOnOvfl)
Restart=fread(f,1,'int32')
res=np.asscalar(Restart)
DispLinLog=fread(f,1,'int32')
DLL=np.asscalar(DispLinLog)
DispTimeAxisFrom=fread(f,1,'int32')
DTAF=np.asscalar(DispTimeAxisFrom)
DispTimeAxisTo=fread(f,1,'int32')
DTAT=np.asscalar(DispTimeAxisTo)
DispCountAxisFrom=fread(f,1,'int32')
DCAF=np.asscalar(DispCountAxisFrom)
DispCountAxisTo=fread(f,1,'int32')
DCAT=np.asscalar(DispCountAxisTo)
#######################################
DispCurveMapTo=['','','','','','','','']
DispCurveShow=['','','','','','','','']
for i in range(8):
    DispCurveMapTo[i]=fread(f,1,'int32')
    DispCurveShow[i]=fread(f,1,'int32')
    #print 'Curve No.:',i
    #print 'MapTo', DispCurveMapTo[i]
    #print 'Show', DispCurveShow[i]
######################################
ParamStart=['','','']
ParamStep=['','','']
ParamEnd=['','','']
for i in range(3):
    ParamStart[i]=fread(f,1,'float32')
    ParamStep[i]=fread(f,1,'float32')
    ParamEnd[i]=fread(f,1,'float32')
    #print "Parameter No.:", i
    #print "Start:", ParamStart[i]
    #print "Step:", ParamStep[i]
    #print "Stop:", ParamEnd[i]
#######################################
RepeatMode=fread(f,1,'int32')
RM=np.asscalar(RepeatMode)
RepeatsPerCurve=fread(f,1,'int32')
RPC=np.asscalar(RepeatsPerCurve)
RepeatTime=fread(f,1,'int32')
RepTime=np.asscalar(RepeatTime)
RepeatWaitTime=fread(f,1,'int32')
RWT=np.asscalar(RepeatWaitTime)
ScriptName=fread(f,20,"S1")
SN=''.join(ScriptName)
#######################################################
####################Header for each Board##############
#######################################################
 
for i in range(NOB):
    #print "Board No.:", NOB-1
    HardwareIdent=(fread(f,16,'S1'))
    HI=''.join(HardwareIdent)
    #print "Hardware Identifier:", HI
    HardwareVersion=fread(f, 8, 'S1')
    HV=''.join(HardwareVersion)
    #print "Hardware Version:",HV
    HardwareSerial=fread(f,1,'int32')
    HWS=np.asscalar(HardwareSerial)
    #print "HW Serial Number:", HWS
    SyncDivider=fread(f,1,'int32')
    SyncDiv=np.asscalar(SyncDivider)
    #print "Sync Divider:", SyncDiv
    CFDZeroCross0=fread(f,1,'int32')
    CFDZC0=np.asscalar(CFDZeroCross0)
    #print "CFD 0 Zero Cross:", CFDZC0, "mV"
    CFDLevel0=fread(f,1,'int32')
    CFDLvl0=np.asscalar(CFDLevel0)
    #print "CFD 0 Discr.:", CFDLvl0,"mV"
    CFDZeroCross1=fread(f,1,'int32')
    CFDZC1=np.asscalar(CFDZeroCross1)
    #print "CFD 1 Zero Cross:",CFDZC1,"mV"
    CFDLevel1=fread(f,1,'int32')
    CFDLvl1=np.asscalar(CFDLevel1)
    #print "CFD 1 Discr.",CFDLvl1,"mV"
    Resolution=fread(f,1,'float32')
    RSLN=np.asscalar(Resolution)
    #print "Resolution:", RSLN, "ns"
    RouterModelCode=fread(f,1,'int32')
    RMC=np.asscalar(RouterModelCode)
    #print "Router Model Code:", RMC
    RouterEnabled=fread(f,1,'int32')
    RtChan1_InputType   = fread(f, 1, 'int32')
    RtChan1_InputLevel   = fread(f, 1, 'int32')
    RtChan1_InputEdge    = fread(f, 1, 'int32')
    RtChan1_CFDPresent   = fread(f, 1, 'int32')
    RtChan1_CFDLevel     = fread(f, 1, 'int32')
    RtChan1_CFDZeroCross = fread(f, 1, 'int32')
# Router Ch2
    RtChan2_InputType   = fread(f, 1, 'int32')
    RtChan2_InputLevel  = fread(f, 1, 'int32')
    RtChan2_InputEdge    = fread(f, 1, 'int32')
    RtChan2_CFDPresent   = fread(f, 1, 'int32')
    RtChan2_CFDLevel     = fread(f, 1, 'int32')
    RtChan2_CFDZeroCross= fread(f, 1, 'int32')
# Router Ch3
    RtChan3_InputType    = fread(f, 1, 'int32')
    RtChan3_InputLevel   = fread(f, 1, 'int32')
    RtChan3_InputEdge   = fread(f, 1, 'int32')
    RtChan3_CFDPresent   = fread(f, 1, 'int32')
    RtChan3_CFDLevel    = fread(f, 1, 'int32')
    RtChan3_CFDZeroCross = fread(f, 1, 'int32')
# Router Ch4
    RtChan4_InputType    = fread(f, 1, 'int32')
    RtChan4_InputLevel  = fread(f, 1, 'int32')
    RtChan4_InputEdge   = fread(f, 1, 'int32')
    RtChan4_CFDPresent  = fread(f, 1, 'int32')
    RtChan4_CFDLevel    = fread(f, 1, 'int32')
    RtChan4_CFDZeroCross = fread(f, 1, 'int32')
#########################################################
######Lines 269-314 go here, but Mark commented out######
#########################################################
CurveIndex=np.zeros(NumberOfCurves)
TimeOfRecording=np.zeros(NumberOfCurves)
#HardwareIdent2=[]
#HardwareVersion=np.zeros(NumberOfCurves)
HardwareSerial2=np.zeros(NumberOfCurves)
SyncDivider2=np.zeros(NumberOfCurves)
CFDZeroCross02=np.zeros(NumberOfCurves)
CFDLevel02=np.zeros(NumberOfCurves)
CFDZeroCross12=np.zeros(NumberOfCurves)
CFDLevel12=np.zeros(NumberOfCurves)
Offset2=np.zeros(NumberOfCurves)
RoutingChannel2=np.zeros(NumberOfCurves)
ExtDevices=np.zeros(NumberOfCurves)
MeasMode=np.zeros(NumberOfCurves)
SubMode2=np.zeros(NumberOfCurves)
P1=np.zeros(NumberOfCurves)
P2=np.zeros(NumberOfCurves)
P3=np.zeros(NumberOfCurves)
RangeNo2=np.zeros(NumberOfCurves)
Resolution2=np.zeros(NumberOfCurves)
Channels2=np.zeros(NumberOfCurves)
Tacq2=np.zeros(NumberOfCurves)
StopAfter=np.zeros(NumberOfCurves)
StopReason=np.zeros(NumberOfCurves)
InpRate0=np.zeros(NumberOfCurves)
InpRate1=np.zeros(NumberOfCurves)
HistCountRate=np.zeros(NumberOfCurves)
IntegralCount=np.zeros(NumberOfCurves)
Reserved=np.zeros(NumberOfCurves)
DataOffset=np.zeros(NumberOfCurves)
RouterModelCode2=np.zeros(NumberOfCurves)
RouterEnabled2=np.zeros(NumberOfCurves)
RtChan_InputType2=np.zeros(NumberOfCurves)
RtChan_InputLevel2=np.zeros(NumberOfCurves)
RtChan_InputEdge2=np.zeros(NumberOfCurves)
RtChan_CFDPresent2=np.zeros(NumberOfCurves)
RtChan_CFDLevel2=np.zeros(NumberOfCurves)
RtChan_CFDZeroCross2=np.zeros(NumberOfCurves)
 
NOC=np.asscalar(NumberOfCurves)
for i in range(NOC):
    CurveIndex[i]=fread(f,1,'int32')
    TimeOfRecording[i]=fread(f,1,'uint32')
    #####Insert here change of time from C time to regular time#####
    HardwareIdent2=fread(f,16,"S1")
    HI2=''.join(HardwareIdent2)
    HardwareVersion2=fread(f,8,"S1")
    HV2=''.join(HardwareVersion2)
    HardwareSerial2[i]=fread(f,1,'int32')
    SyncDivider2[i]=fread(f,1,'int32')
    CFDZeroCross02[i]=fread(f,1,'int32')
    CFDLevel02[i]=fread(f,1,'int32')
    CFDZeroCross12[i]=fread(f,1,'int32')
    CFDLevel12[i]=fread(f,1,'int32')
    Offset2[i]=fread(f,1,'int32')
    RoutingChannel2[i]=fread(f,1,'int32')
    ExtDevices[i]=fread(f,1,'int32')
    MeasMode[i]=fread(f,1,'int32')
    SubMode2[i]=fread(f,1,'int32')
    P1[i]=fread(f,1,'float32')
    P2[i]=fread(f,1,'float32')
    P3[i]=fread(f,1,'float32')
    RangeNo2[i]=fread(f,1,'int32')
    Resolution2[i]=fread(f,1,'float32')
    Channels2[i]=(fread(f,1,'int32'))
    Tacq2[i]=fread(f,1,'int32')
    StopAfter[i]=fread(f,1,'int32')
    StopReason[i]=fread(f,1,'int32')
    InpRate0[i]=fread(f,1,'int32')
    InpRate1[i]=fread(f,1,'int32')
    HistCountRate[i]=fread(f,1,'int32')
    IntegralCount[i]=fread(f,1,'int64')
    Reserved[i]=fread(f,1,'int32')
    DataOffset[i]=fread(f,1,'int32')
    RouterModelCode2[i]     = fread(f, 1, 'int32')
    RouterEnabled2[i]       = fread(f, 1, 'int32')
    RtChan_InputType2[i]    = fread(f, 1, 'int32')
    RtChan_InputLevel2[i]   = fread(f, 1, 'int32')
    RtChan_InputEdge2[i]    = fread(f, 1, 'int32')
    RtChan_CFDPresent2[i]   = fread(f, 1, 'int32')
    RtChan_CFDLevel2[i]     = fread(f, 1, 'int32')
    RtChan_CFDZeroCross2[i] = fread(f, 1, 'int32')
#Counts=np.zeros(NumberOfCurves)
Channels2=list(Channels2)
for i in range(len(Channels2)):
    Channels2[i]=int(Channels2[i])
for i in range(NOC):
    a=f.seek(DataOffset[i],0)
    Counts=(fread(f,Channels2[i],'uint32'))
Peak=max(Counts)
Data=[]
DataSub=[]
Data.append(True)
Data.append(NOC)
Data.append(DataSub)
print Data



