import os
class CustomError(Exception):
        pass
os.chdir('C:\Users\Minhal\Desktop')  ###Change Directories###
a=[0,0,0]   ###Dummy for white/black selection###

if sum(a)==3 and not os.path.exists('Analysis\White'):
	os.makedirs('Analysis\White')
elif sum(a)==0 and not os.path.exists('Analysis\Black'):
	os.makedirs('Analysis\Black')
else:
        raise CustomError('DefaultFigColour is neither white nor black -- this case is not yet supported by the program, please retry')



if 'MainData' in globals():    ###Existence Checker###
    print "********************************************"
    print "Data Detected in Memory - Skipping Data Load"
    print "********************************************"
else:
        print "Loading your data"

