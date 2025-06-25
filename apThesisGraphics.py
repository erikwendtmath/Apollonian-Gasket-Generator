# the graphics needed for my thesis
import apMaker as ap
import numpy as np
import matplotlib.pyplot as plt

# start with just one set of Soddy circles
pt1, pt2, pt3 = 0, 1, .5+.5j
C1,C2,C3 = ap.triangle2Soddy(pt1,pt2,pt3)
# gasket = [C1,C2,C3]
# ap.plotGasket(gasket)
# gasket.extend(ap.descarte(C1,C2,C3))
# ap.plotGasket(gasket)

# now assemble the entire gasket
n = 8
gasket = ap.makeGasket(C1,C2,C3,n)
fig, ax = ap.plotGasket(gasket,normalize=True)
plt.show()