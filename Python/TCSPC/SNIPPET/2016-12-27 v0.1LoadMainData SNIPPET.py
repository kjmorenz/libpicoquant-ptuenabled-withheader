import os
if "MainData" in globals():  ###MainData declared globally, of course?###
    LoadSkip=True
    print "**********************************************************"
    print "Data Detected in Memory - Skipping Data Load"
    print "**********************************************************"
    dummy=raw_input('Press <Enter> to continue')
    print "Continuing program execution..."
    del dummy
else:
    LoadSkip=False
    print "**********************************************************"
    print "No Data Detected in Memory"
    print "--> Proceeding to Load Data..."
    print "**********************************************************"
	
if LoadSkip==False:
    MainData=None
PathD='C:\Users\Minhal\Desktop'
Files=os.listdir(PathD)
print Files
		
