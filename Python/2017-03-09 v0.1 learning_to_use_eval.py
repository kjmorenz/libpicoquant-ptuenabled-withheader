'''def perim(a):
    return 4*a

def area(a):
    return 1*a
prop=raw_input("Type a function: ")

for a in range(1,5):
    if (prop=='perim(a)'):
        print(eval(prop))
    elif (prop=='area(a)'):
        print (eval(prop))
    else:
        print ("wrong function")
        break
'''
from math import *
user_func=raw_input("Type a function: y= ")
for x in range(10):
    print x, eval(user_func)
