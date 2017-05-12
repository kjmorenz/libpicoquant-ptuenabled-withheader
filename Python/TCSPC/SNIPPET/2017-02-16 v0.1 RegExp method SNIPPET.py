
import re
#From a file or list, strip out non-header entries and append
#all that begin with two numbers to a list

def regexp(folder, filenames, fileExtension):
    newlist = []
    
    header = re.compile('\d\d-\d\d\s-\s')

    for item in filenames:
        filename = folder + item + fileExtension
        file = open(filename)
        for line in file.readlines():
            if header.match(line) != None:
                newlist.append(line)
        file.close()

    return newlist

files = ["2015-07-28 - Experimental Log", "2015-08-26 - Experimental Log"]
folder = "C:\\Users\\Karen\\Dropbox (WilsonLab)\\WilsonLab Team Folder\\Programs/2016-12-21 - Mark's Matlab Data Analysis Package\\test data\\"
fileExtension = ".txt"
print(regexp(folder, files, fileExtension))
