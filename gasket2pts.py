# - given a gasket, or just a general collection of circles, generate pts from the gasket
# - want this to work even if there are fewer pts than the number of circles
# - controls the apx number of points, since we do not want to take away random pts 
# unless specified or fewer pts than circles
# TODO: case where there are fewer points than circles

import apMaker as ap # need circle class
import numpy as np

def gasket2pts(gasket,apx_numpts, errtype = None,seed=0):
    numcircs = len(gasket)
    if apx_numpts > numcircs:
        ptsPerCirc = np.ceil(apx_numpts/numcircs) # want same number of pts on each circle
        ptsPerCirc = int(ptsPerCirc) # cast as integer
        z = np.exp(2*np.pi*1j*np.linspace(0,1,ptsPerCirc))
    
    pts = []
    for circ in gasket:
        circpts = circ.center+z*circ.radius
        pts.append(circpts)
    return pts

