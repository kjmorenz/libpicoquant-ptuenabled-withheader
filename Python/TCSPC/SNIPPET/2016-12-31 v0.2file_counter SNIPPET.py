import os
PathD='C:\Users\Minhal\Desktop'
Files=os.listdir(PathD)


ndf=0
FileList=[]
for i in range(len(Files)):
    if len(Files[i])>=8 and Files[i][-8:-1] == 'Data.ph':
        ndf+=1
    if Files[i][-8:-1]=='Data.ph':
        FileList.append(Files[i])
        
        
if ndf==0:
    print "No .phd files detected"

print ndf, FileList
