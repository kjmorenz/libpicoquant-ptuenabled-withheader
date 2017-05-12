
import re
#From a file or list, strip out non-header entries and append
#all that begin with two numbers to a list

def regexpLogFiles(folder, filenames):
    newlist = []
    
    header = re.compile('\d\d-\d\d\s-\s')

    for item in filenames:
        filename = folder + item 
        file = open(filename)
        for line in file.readlines():
            if header.match(line) != None:
                if line[-1] == '\n':
                    line = line[:-1]
                newlist.append(line)
        file.close()

    return newlist

files = ["2015-07-28 - Experimental Log.txt", "2015-08-26 - Experimental Log.txt"]
folder = "C:\\Users\\Karen\\Dropbox (WilsonLab)\\WilsonLab Team Folder\\Programs/2016-12-21 - Mark's Matlab Data Analysis Package\\test data\\"

print(regexpLogFiles(folder, files))
