from numpy import *
from matplotlib import pyplot as plt


### Define Constants ###

me=.13
mh=.45

### Set Radius Values ###

R=arange(10,35,1)

### Define Function ###

def f(x):
    return (1./x**2)*((1/me)+(1/mh))-(1./x)

### Plot The Result ###

plt.plot(R,f(R))
plt.show()
