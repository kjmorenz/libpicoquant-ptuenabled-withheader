import os
from array import array
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
RepeatWaitTime=fread(f,1,'int32')
ScriptName=fread(f,20,"S1")
SN=''.join(ScriptName)

HardwareIdent=fread(f,16,'S1')
HI=''.join(HardwareIdent)
HardwareVersion=fread(f, 8, 'S1')
HV=''.join(HardwareVersion)
HardwareSerial=fread(f,1,'int32')
SyncDivider=fread(f,1,'int32')
CFDZeroCross0=fread(f,1,'int32')
CFDLevel0=fread(f,1,'int32')
CFDZeroCross1=fread(f,1,'int32')
CFDLevel1=fread(f,1,'int32')
Resolution=fread(f,1,'float32')
RouterModelCode=fread(f,1,'int32')
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

for i in range(NumberOfCurves):
    CurveIndex[i]=fread(f,1,'int32')
    TimeOfRecording[i]=fread(f,1,'uint32')
    DummyHardwareIdent[i]=fread(16,'S1')
    DummyHardwareVersion[i]=fread(f,8,'S1')
    print DummyHardwareVersion
    DummyHardwareSerial[i]=fread(f,1,'int32')
    DummySyncDivider=fread(f,1,'int32')
    DummyCFDZeroCross0[i] = fread(f, 1, 'int32');
    DummyCFDLevel0[i] = fread(f, 1, 'int32')
    DummyCFDZeroCross1[i] = fread(f, 1, 'int32')
    DummyCFDLevel1[i] = fread(f, 1, 'int32')
    DummyOffset[i] = fread(f, 1, 'int32');
    RoutingChannel[i] = fread(f, 1, 'int32');
    ExtDevices[i] = fread(f, 1, 'int32');
    MeasMode[i] = fread(f, 1, 'int32');
    SubMode[i] = fread(f, 1, 'int32');
    P1[i] = fread(f, 1, 'float');
    P2[i] = fread(f, 1, 'float');
    P3[i] = fread(f, 1, 'float');
    RangeNo[i] = fread(f, 1, 'int32');
    Resolution[i] = fread(f, 1, 'float');
    Channels[i] = fread(f, 1, 'int32');
    DummyTacq[i] = fread(f, 1, 'int32');
    StopAfter[i] = fread(f, 1, 'int32');
    StopReason[i] = fread(f, 1, 'int32');
    InpRate0[i] = fread(f, 1, 'int32');
    InpRate1[i] = fread(f, 1, 'int32');
    HistCountRate[i] = fread(f, 1, 'int32');
    IntegralCount[i] = fread(f, 1, 'int64');
    Reserved[i] = fread(f, 1, 'int32');
    DataOffset[i] = fread(f, 1, 'int32');
    RouterModelCode[i]     = fread(f, 1, 'int32');
    RouterEnabled[i]       = fread(f, 1, 'int32');
    RtChan_InputType[i]    = fread(f, 1, 'int32');
    RtChan_InputLevel[i]   = fread(f, 1, 'int32');
    RtChan_InputEdge[i]   = fread(f, 1, 'int32');
    RtChan_CFDPresent[i]   = fread(f, 1, 'int32');
    RtChan_CFDLevel[i]     = fread(f, 1, 'int32');
    RtChan_CFDZeroCross[i] = fread(f, 1, 'int32');

