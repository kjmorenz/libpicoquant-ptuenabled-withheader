import os
from array import array  #Don't explicitly need this, just in case
import numpy as np
os.chdir('C:\Users\Minhal\Desktop')
class CustomError(Exception):
    pass

def fread(f, n, dtype):
    """A clone of MATLAB's 'fread' function.  Numpy must be imported
    f--> Filename (Including extension)
    n--> Number of BYTES to be read in
    dtype--> Data Type, as seen by NUMPY, not Python default"""
    if dtype is np.str:
        dt=np.uint8
    else:
        dt=dtype

    data_array=np.fromfile(f, dt, n)
    #data_array.shape=(n,1)
    return data_array

f=open('2015-08-26-SWIRTCPSC-Data.phd','rb')

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
NumberOfCurves=np.asscalar(fread(f,1,"int32"))
BitsPerHistoBin=np.asscalar(fread(f,1,'int32'))
RoutingChannels=np.asscalar(fread(f,1,'int32'))
NumberOfBoards=np.asscalar(fread(f,1,'int32'))
ActiveCurve=np.asscalar(fread(f,1,'int32'))
MeasurementMode=np.asscalar(fread(f,1,'int32'))
SubMode=np.asscalar(fread(f,1,'int32'))
RangeNo=np.asscalar(fread(f,1,'int32'))
Offset=np.asscalar(fread(f,1,'int32'))
Tacq=np.asscalar(fread(f,1,'int32'))
StopAt=np.asscalar(fread(f,1,'int32'))
StopOnOvfl=np.asscalar(fread(f,1,'int32'))
Restart=np.asscalar(fread(f,1,'int32'))
DispLinLog=np.asscalar(fread(f,1,'int32'))
DispTimeAxisFrom=np.asscalar(fread(f,1,'int32'))
DispTimeAxisTo=np.asscalar(fread(f,1,'int32'))
DispCountAxisFrom=np.asscalar(fread(f,1,'int32'))
DispCountAxisTo=np.asscalar(fread(f,1,'int32'))
##################################################################
DispCurveMapTo=['','','','','','','','']
DispCurveShow=['','','','','','','','']
for i in range(8):
    DispCurveMapTo[i]=np.asscalar(fread(f,1,'int32'))
    DispCurveShow[i]=np.asscalar(fread(f,1,'int32'))
    print "Curve No.:",i
    print "MapTo:", DispCurveMapTo[i]
    print "Show:",DispCurveShow[i]
###################################################################
ParamStart=['','','']
ParamStep=['','','']
ParamEnd=['','','']
for i in range(3):
    ParamStart[i]=np.asscalar(fread(f,1,'float32'))
    ParamStep[i]=np.asscalar(fread(f,1,'float32'))
    ParamEnd[i]=np.asscalar(fread(f,1,'float32'))
    print "Parameter No.:", i
    print "Start:", ParamStart[i]
    print "Step:",ParamStep[i]
    print "End:",ParamEnd[i]
##################################################################
RepeatMode=np.asscalar(fread(f,1,'int32'))
RepeatsPerCurve=np.asscalar(fread(f,1,'int32'))
RepeatTime=np.asscalar(fread(f,1,'int32'))
RepeatWaitTime=np.asscalar(fread(f,1,'int32'))
ScriptName=fread(f,20,"S1")
SN=''.join(ScriptName)
#################################################################
#################################################################
#####################Header for each board#######################
#################################################################

###Actually should pre-allocate each variable that takes
###on an int32 value, and then have the loop execute
###but for now this works since NumberOfBoards=1

for i in range(NumberOfBoards):
    HardwareIdent=fread(f,16,'S1')
    HI=''.join(HardwareIdent)
    HardwareVersion=fread(f, 8, 'S1')
    HV=''.join(HardwareVersion)
    HardwareSerial=np.asscalar(fread(f,1,'int32'))
    SyncDivider=np.asscalar(fread(f,1,'int32'))
    CFDZeroCross0=np.asscalar(fread(f,1,'int32'))
    CFDLevel0=np.asscalar(fread(f,1,'int32'))
    CFDZeroCross1=np.asscalar(fread(f,1,'int32'))
    CFDLevel1=np.asscalar(fread(f,1,'int32'))
    Resolution=np.asscalar(fread(f,1,'float32'))
    RouterModelCode=np.asscalar(fread(f,1,'int32'))
    RouterEnabled=np.asscalar(fread(f,1,'int32'))
    RtChan1_InputType   = np.asscalar(fread(f, 1, 'int32'))
    RtChan1_InputLevel   = np.asscalar(fread(f, 1, 'int32'))
    RtChan1_InputEdge    = np.asscalar(fread(f, 1, 'int32'))
    RtChan1_CFDPresent   = np.asscalar(fread(f, 1, 'int32'))
    RtChan1_CFDLevel     = np.asscalar(fread(f, 1, 'int32'))
    RtChan1_CFDZeroCross = np.asscalar(fread(f, 1, 'int32'))
    # Router Ch2
    RtChan2_InputType   = np.asscalar(fread(f, 1, 'int32'))
    RtChan2_InputLevel  = np.asscalar(fread(f, 1, 'int32'))
    RtChan2_InputEdge    = np.asscalar(fread(f, 1, 'int32'))
    RtChan2_CFDPresent   = np.asscalar(fread(f, 1, 'int32'))
    RtChan2_CFDLevel     = np.asscalar(fread(f, 1, 'int32'))
    RtChan2_CFDZeroCross= np.asscalar(fread(f, 1, 'int32'))
    # Router Ch3
    RtChan3_InputType    = np.asscalar(fread(f, 1, 'int32'))
    RtChan3_InputLevel   = np.asscalar(fread(f, 1, 'int32'))
    RtChan3_InputEdge   = np.asscalar(fread(f, 1, 'int32'))
    RtChan3_CFDPresent   = np.asscalar(fread(f, 1, 'int32'))
    RtChan3_CFDLevel    = np.asscalar(fread(f, 1, 'int32'))
    RtChan3_CFDZeroCross = np.asscalar(fread(f, 1, 'int32'))
    # Router Ch4
    RtChan4_InputType    =np.asscalar( fread(f, 1, 'int32'))
    RtChan4_InputLevel  = np.asscalar(fread(f, 1, 'int32'))
    RtChan4_InputEdge   = np.asscalar(fread(f, 1, 'int32'))
    RtChan4_CFDPresent  = np.asscalar(fread(f, 1, 'int32'))
    RtChan4_CFDLevel    = np.asscalar(fread(f, 1, 'int32'))
    RtChan4_CFDZeroCross = np.asscalar(fread(f, 1, 'int32'))
#########################################################
######Lines 269-314 go here, but Mark commented out######
#########################################################

#############################################################
#############################################################
##########Headers for each histogram (curve)#################
#############################################################
#############################################################
CurveIndex=np.zeros(NumberOfCurves)
TimeOfRecording2=np.zeros(NumberOfCurves)
HardwareSerial2=np.zeros(NumberOfCurves)
SyncDivider2=np.zeros(NumberOfCurves)
CFDZeroCross02=np.zeros(NumberOfCurves)
CFDLevel02=np.zeros(NumberOfCurves)
CFDZeroCross12=np.zeros(NumberOfCurves)
CFDLevel12=np.zeros(NumberOfCurves)
P1=np.zeros(NumberOfCurves)
P2=np.zeros(NumberOfCurves)
P3=np.zeros(NumberOfCurves)
Offset2=np.zeros(NumberOfCurves)
RoutingChannel2=np.zeros(NumberOfCurves)
ExtDevices2=np.zeros(NumberOfCurves)
MeasMode2=np.zeros(NumberOfCurves)
SubMode2=np.zeros(NumberOfCurves)
RangeNo2=np.zeros(NumberOfCurves)
Resolution2=np.zeros(NumberOfCurves)
Channels2=np.zeros(NumberOfCurves)
Tacq2=np.zeros(NumberOfCurves)
StopAfter2=np.zeros(NumberOfCurves)
StopReason2=np.zeros(NumberOfCurves)
InpRate02=np.zeros(NumberOfCurves)
InpRate12=np.zeros(NumberOfCurves)
HistCountRate2=np.zeros(NumberOfCurves)
IntegralCount2=np.zeros(NumberOfCurves)
Reserved2 =np.zeros(NumberOfCurves)
DataOffset2=np.zeros(NumberOfCurves)
RouterModelCode2=np.zeros(NumberOfCurves)
RouterEnabled2=np.zeros(NumberOfCurves)
RtChan_InputType2=np.zeros(NumberOfCurves)
RtChan_InputLevel2=np.zeros(NumberOfCurves)
RtChan_InputEdge2=np.zeros(NumberOfCurves)
RtChan_CFDPresent2=np.zeros(NumberOfCurves)
RtChan_CFDLevel2=np.zeros(NumberOfCurves)
RtChan_CFDZeroCross2=np.zeros(NumberOfCurves)


for i in range(NumberOfCurves):
    CurveIndex[i]=fread(f,1,'int32')
    TimeOfRecording2[i]=fread(f,1,'uint32')
    ####Insert code here to convert from C time to normal time###
    HardwareIdent2=fread(f,16,'S1')
    HI2=''.join(HardwareIdent2)
    HardwareVersion2=fread(f,8,'S1')
    HV2=''.join(HardwareVersion2)
    HardwareSerial2[i]=fread(f,1,'int32')
    SyncDivider2[i]=fread(f,1,'int32')
    CFDZeroCross02[i] = fread(f, 1, 'int32')
    CFDLevel02[i] = fread(f, 1, 'int32')
    CFDZeroCross12[i] = fread(f, 1, 'int32')
    CFDLevel12[i] = fread(f, 1, 'int32')
    Offset2[i] = fread(f, 1, 'int32');
    RoutingChannel2[i] = fread(f, 1, 'int32')
    ExtDevices2[i] = fread(f, 1, 'int32')
    MeasMode2[i] = fread(f, 1, 'int32')
    SubMode2[i] = fread(f, 1, 'int32')
    P1[i] = fread(f, 1, 'float64')
    P2[i] = fread(f, 1, 'float64')
    P3[i] = fread(f, 1, 'float64')
    RangeNo2[i] = fread(f, 1, 'int32')
    Resolution2[i] = fread(f, 1, 'float')
    Channels2[i] = fread(f, 1, 'int32')
    Tacq2[i] = fread(f, 1, 'int32')
    StopAfter2[i] = fread(f, 1, 'int32')
    StopReason2[i] = fread(f, 1, 'int32')
    InpRate02[i] = fread(f, 1, 'int32')
    InpRate12[i] = fread(f, 1, 'int32')
    HistCountRate2[i] = fread(f, 1, 'int32')
    IntegralCount2[i] = fread(f, 1, 'int64')
    Reserved2[i] = fread(f, 1, 'int32')
    DataOffset2[i] = fread(f, 1, 'int32')
    RouterModelCode2[i]     = fread(f, 1, 'int32')
    RouterEnabled2[i]       = fread(f, 1, 'int32')
    RtChan_InputType2[i]    = fread(f, 1, 'int32')
    RtChan_InputLevel2[i]   = fread(f, 1, 'int32')
    RtChan_InputEdge2[i]   = fread(f, 1, 'int32')
    RtChan_CFDPresent2[i]   = fread(f, 1, 'int32')
    RtChan_CFDLevel2[i]     = fread(f, 1, 'int32')
    RtChan_CFDZeroCross2[i] = fread(f, 1, 'int32')

