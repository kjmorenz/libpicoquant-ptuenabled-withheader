
import os
from array import array
import numpy as np
os.chdir('C:\Users\Minhal\Desktop')
class CustomError(Exception):
    pass

def fread(f, n, dtype):
    """A clone of MATLAB's 'fread' function.  Numpy must be imported"""
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
CreatorName=fread(f, 17, "S1")
CN=''.join(CreatorName)
CreatorVersion=fread(f,12,"S1")
CV=''.join(CreatorVersion)
FileTime=fread(f, 18, "S1")
FT=''.join(FileTime)
CRLF=fread(f,2,"S1")
clf=''.join(CRLF)
Comment=fread(f,256,"S1")
cm=''.join(Comment)
NumberOfCurves=fread(f,1,"int32")
BitsPerHistoBin=fread(f,1,'int32')
RoutingChannels=fread(f,1,'int32')
NumberOfBoards=fread(f,1,'int32')
ActiveCurve=fread(f,1,'int32')
MeasurementMode=fread(f,1,'int32')
SubMode=fread(f,1,'int32')
RangeNo=fread(f,1,'int32')
Offset=fread(f,1,'int32')
Tacq=fread(f,1,'int32')
StopAt=fread(f,1,'int32')
StopOnOvfl=fread(f,1,'int32')
Restart=fread(f,1,'int32')
DispLinLog=fread(f,1,'int32')
DispTimeAxisFrom=fread(f,1,'int32')
DispTimeAxisTo=fread(f,1,'int32')
DispCountAxisFrom=fread(f,1,'int32')
DispCountAxisTo=fread(f,1,'int32')
DispCurveMapTo=['','','','','','','','']
DispCurveShow=['','','','','','','','']
for i in range(8):
    DispCurveMapTo[i]=fread(f,1,'int32')
    DispCurveShow[i]=fread(f,1,'int32')
ParamStart=['','','']
ParamStep=['','','']
ParamEnd=['','','']
for i in range(3):
    ParamStart[i]=fread(f,1,'float64')
    ParamStep[i]=fread(f,1,'float64')
    ParamEnd[i]=fread(f,1,'float64')

RepeatMode=fread(f,1,'int32')
RepeatsPerCurve=fread(f,1,'int32')
RepeatTime=fread(f,1,'int32')
RepeatWaitTime=fread(f,1,'int32')
ScriptName=fread(f,20,"S1")
SN=''.join(ScriptName)
'''HardwareIdent=['']
for i in range(len(NumberOfBoards)):
    HardwareIdent[i]=fread(f,16,"S1")'''

