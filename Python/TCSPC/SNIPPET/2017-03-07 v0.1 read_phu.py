import os
import numpy as np
class CustomError(Exception):
    pass
os.chdir('C:\Users\Minhal\Desktop')
def hex2dec(n):
    '''Return the integer value of a hexadecimal string n'''
    return int(n,16)
def fread(f,n,dtype):
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
f=open("2017-03-07 Mark's CdSe Dots Ensemble.phu",'rb')

tyEmpty8      = hex2dec('FFFF0008');
tyBool8       = hex2dec('00000008');
tyInt8        = hex2dec('10000008');
tyBitSet64    = hex2dec('11000008');
tyColor8      = hex2dec('12000008');
tyFloat8      = hex2dec('20000008');
tyTDateTime   = hex2dec('21000008');
tyFloat8Array = hex2dec('2001FFFF');
tyAnsiString  = hex2dec('4001FFFF');
tyWideString  = hex2dec('4002FFFF');
tyBinaryBlob  = hex2dec('FFFFFFFF');

Magic=fread(f,8,'S1')
MG=''.join(Magic)

if MG !='PQHISTO':
    raise CustomError('Warning: This is not a PHU file.  Aborting.')
Version=fread(f,8,'S1')
VRSN=''.join(Version)
print VRSN

def empty8():
    fread(f,1,'int64')
    print ("<Empty>")
def bool8():
    TagInt=fread(f,1,'int64')
    if TagInt==0:
        print("FALSE")
        EvalName=False
    else:
        print("TRUE")
        EvalName=True
def int8():
    TagInt=fread(f,1,'int64')
    print (TagInt)
    EvalName=TagInt
def BitSet64():
    TagInt=fread(f,1,'int64')
    EvalName=TagInt
def color8():
    TagInt=fread(f,1,'int64')
    print (TagInt)
    EvalName=TagInt
def float8():
    fread(f, 1,'float64')
    print(TagInt)
def floatarray():
    TagInt=fread(f, 1,'int64')
    print ('<Float array with %d entries>', TagInt/8)
    f.seek(TagInt,1) 
def TdateTime():
    TagFloat=fread(f,1,'float64')
    ###Convert to datestring still needs to be written###
def ansistring():
    TagInt=fread(f,1,'int64')
    TagString=fread(f,TagInt,'S1')
    


while True:
    TagIdent=fread(f,32,'S1')
    TI=''.join(TagIdent)
    print TI
    #TagIdent=(TagIdent(TagIdent~=))  #This is the original MATLAB, not
    #sure what it does
    TagIdx=fread(f,1,'int32')
    TagIdx=np.asscalar(TagIdx)
    print TagIdx
    TagType=fread(f,1,'uint32')
    print TagType
    if TagIdx>-1:
        EvalName=[TI + '(' + str(TagIdx+1) + ')']
    else:
        EvalName=TI


