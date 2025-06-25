import numpy as np
import apMaker as ap
import matplotlib.pyplot as plt

# test gasket2pts

# get Soddy circle centers to create the gasket
def genRandCpxPt(real_min, real_max, imag_min, imag_max,numpts):
    real_part = np.random.uniform(real_min, real_max,numpts)
    imag_part = np.random.uniform(imag_min, imag_max,numpts)
    cpxPts = real_part+1j*imag_part
    return cpxPts

numpts = 36

# Define the box boundaries
real_min, real_max = -1.0, 1.0
imag_min, imag_max = -1.0, 1.0

pts = genRandCpxPt(real_min,real_max,imag_min,imag_max,numpts)
pts = np.array(pts)
pts = np.reshape(pts,(int(len(pts)/3),3))
# plt.plot(pts.real,pts.imag,'b.')
# plt.show()

print(pts)

# we want to plot each of these to check the descartes program
figure = plt.figure(figsize=(int(numpts/9),3))
i = 1 # startin index for subplots
for row in pts:
    C1,C2,C3 = ap.triangle2Soddy(row[0],row[1],row[2])
    circs = [C1,C2,C3]
    # C4,C5 = ap.descarte(C1,C2,C3)
    circs.extend(ap.descarte(C1,C2,C3))
    ax = plt.subplot(int(numpts/9),3,i)
    t = np.linspace(0,2*np.pi,100)
    for k in range(5): # plot each Soddy circle
        ax.plot((circs[k].center+circs[k].radius*np.exp(1j*t)).real,
                 (circs[k].center+circs[k].radius*np.exp(1j*t)).imag,'b-')
        
    i+=1

plt.show()