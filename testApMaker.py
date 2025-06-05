# test the program to make Apollonian gaskets

import apMaker as ap
import numpy as np
import matplotlib.pyplot as plt

# start with just one set of Soddy circles
pt1, pt2, pt3 = -1, 1, .2j
C1,C2,C3 = ap.triangle2Soddy(pt1,pt2,pt3)
n = 2 # number of generations
gasket = ap.makeGasket(C1,C2,C3,n)
ap.plotGasket(gasket)