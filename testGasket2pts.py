# test the gasket2pts program
import matplotlib.pyplot as plt
import apMaker as ap
import numpy as np
import gasket2pts as g2p

# random pt generator
def genRandCpxPt(real_min, real_max, imag_min, imag_max,numpts):
    real_part = np.random.uniform(real_min, real_max,numpts)
    imag_part = np.random.uniform(imag_min, imag_max,numpts)
    cpxPts = real_part+1j*imag_part
    return cpxPts

real_min, real_max, imag_min, imag_max = -1, 1, -1 ,1
z1, z2, z3 = genRandCpxPt(real_min,real_max,imag_min,imag_max,3)
# make Soddy circles
C1,C2,C3 = ap.triangle2Soddy(z1,z2,z3)

# now make a gasket
gen = 5
gasket = ap.makeGasket(C1,C2,C3,gen)

numpts = 20*len(gasket)
pts = g2p.gasket2pts(gasket,numpts)
plt.plot(np.real(pts),np.imag(pts),'b.')
plt.show()