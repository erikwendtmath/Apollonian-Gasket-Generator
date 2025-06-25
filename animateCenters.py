# simple animation of the centers of points in the gasket
import numpy as np
import apMaker as ap
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# generate intial Soddy circles
pt1, pt2, pt3 = 0, 1, .5+(np.sqrt(3)/2)*1j

# create the curve C3 will travel around
t = np.linspace(0,2*np.pi,100)
curve = 0.4*np.exp(1j*t)+0.3*np.sin(t)

# parameterized gaskets
n= 3
gasket_family = []
for pt in curve:
    C1,C2,C3 = ap.triangle2Soddy(pt1,pt2,pt3+pt)
    gasket_family.append(ap.makeGasket(C1,C2,C3,n))


fig, ax = plt.subplots()

def update(frame):
    gasket = gasket_family[frame]
    centList = [circ.center for circ in gasket]
    ax.plot(np.real(centList), np.imag(centList),'b.')
    return []

anim = FuncAnimation(fig,update,frames=len(gasket_family),interval=50)
plt.show()