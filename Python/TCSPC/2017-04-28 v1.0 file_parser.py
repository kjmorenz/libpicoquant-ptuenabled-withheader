
class LoadError(Exception):
    pass
import numpy as np
import os
FilePath=('D:/Dropbox (WilsonLab)/WilsonLab Team Folder/Data/Minhal/TCSPC Comission/')
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
        print "<Empty>"
    elif TagTyp==tyBool8:
        TagInt=fread(f,1,'int64')
        if TagInt==0:
            print "FALSE"
            exec(EvalName+'=False')
        else:
            print "TRUE"
            exec(EvalName+'=True')
    elif TagTyp==tyInt8:
        TagInt=fread(f,1,'int64')
        print '%d' %TagInt
        exec(EvalName+'=TagInt')
    elif TagTyp==tyBitSet64:
        TagInt==fread(f,1,'int64')
        print '%X' %TagInt
        exec(EvalName+'=TagInt')
    elif TagTyp==tyColor8:
        TagInt=fread(f,1,'int64')
        print "%X" %TagInt
        exec(EvalName+'=TagInt')
    elif TagTyp==tyFloat8:
        TagFloat=fread(f,1,'float64')
        print "%E" %TagFloat
        exec(EvalName+'=TagFloat')
    elif TagTyp==tyFloat8Array:
        TagInt=fread(f,1,'int64')
        print ("Float array with %d entries" %(TagInt/8))
    elif TagTyp==tyTDateTime:
        TagFloat=fread(f,1,'float64')
        print ('%s' %TagFloat)
        exec(EvalName+'=TagFloat')
    elif TagTyp==tyAnsiString:
        TagInt=fread(f,1,'int64')
        TagString=fread(f,TagInt,"S1")
        print ("%s" %TagString)
        exec(EvalName+'=TagString')
        if TagIdx>-1:
            EvalName=TagIdent + '(' +str(TagIdx+1) + ',:)'
        
    elif TagTyp==tyWideString:
        TagInt=fread(f,1,'int64')
        TagString=fread(f,TagInt,"S1")
        print ("%s" %TagString)
        if TagIdx>-1:
            EvalName=TagIdent + '(' + str(TagIdx+1) + ',:)'
        exec(EvalName+'= TagString')
    elif TagTyp==tyBinaryBlob:
        TagInt=fread(f,1,'int64')
        print ("Binary Blob with %d Bytes" %TagInt)
    if TagIdent=='Header_End':
        break
    




