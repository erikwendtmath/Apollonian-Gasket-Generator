# in this file we create a program to visualize Apollonian gasket. 
# This uses complex circles and Descarte's theorem
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class circle:

    def __init__(self,center,radius):
        self.center = center
        self.radius = radius
        
        # needed to generate further circles
        self.generation = None
        self.firstTangencies = None

    def __str__(self):
        return "Center: %s Radius: %s" % (self.center,self.radius)
    
    def as_dict(self):
        return {'center': self.center, 'radius': self.radius, 'generation': self.generation, 
                'firstTangencies': self.firstTangencies}

# go from three points to their Soddy circles (mutually tangent)
def triangle2Soddy(p1,p2,p3):
    # get side lengaths
    a, b, c = abs(p1-p2), abs(p1-p3), abs(p2-p3)
    s = 0.5*(a+b+c) # semiperimeter
    C1 = circle(p1,s-c)
    C2 = circle(p2,s-b)
    C3 = circle(p3,s-a)
    return C1,C2,C3

# a function to check if circles are mutually tangent
def isTangent(circle1,circle2):

    # need to verify that r_1+r_2 = |c_1-c_2|
    r1, r2 = circle1.radius, circle2.radius

    c1,c2  = circle1.center, circle2.center

    if math.isclose(abs(c1-c2),r1+r2):# no containment tangency
        return True
    elif (abs(c1-c2) < max(r1,r2)) & math.isclose(abs(c1-c2),abs(r1-r2)): # containment tangency
        return True
    else:
        return False

# given three mutually tangent circles, find their signed curvatures
def findCurvature(circle1,circle2,circle3):
    circles = [circle1,circle2,circle3]
    r1, r2 ,r3 = circle1.radius, circle2.radius, circle3.radius
    klist = []
    
    maxrad = max(r1,r2,r3)
    # check containment between circles
    for k in range(3):
        if circles[k].radius == maxrad:
            if min(abs(circles[k].center - circles[(k+1)%3].center), abs(circles[k].center - circles[(k+2)%3].center))<maxrad:
                klist.append(-1/circles[k].radius)
            else:
                klist.append(1/circles[k].radius)
        else:
            klist.append(1/circles[k].radius)
    return klist

# Now implement Descartes' formula
def descarte(c1,c2,c3):
    # Inputs: 
    # c1, c2, c3 - 3 mutually tangent circles 
    # type - variable argument. If included, output both mutually tangent circles

    # Outputs: 
    # c4 - new circle with smaller radius 
    # c5 - new circle with larger radius

    # return nothing if the circles are not tangent. TODO: maybe throw an error here
    if not(isTangent(c1,c2) & isTangent(c2,c3) & isTangent(c3,c1)): 
        return None
    
    # get curvatures
    k1, k2, k3 = findCurvature(c1,c2,c3)

    # by descartes', k4 = k1+k2+k3+-2sqrt(k1k2+k1k3+k2k3)
    k4 = k1+k2+k3+2*np.sqrt(k1*k2+k1*k3+k2*k3) # curvature for two circles
    k5 = k1+k2+k3-2*np.sqrt(k1*k2+k1*k3+k2*k3) 
    klist = [k4, k5] # potential curvatures --- note that some may be negative

    # the centers are given by another formula (see Wikipedia) 
    # each potential curvature corresponds to 2 potential circles
    clist = [] # list of tangent circles
    for k in klist:
        # generate two cirlces
        cent1 = ((c1.center*k1+c2.center*k2+c3.center*k3+
                   2*np.sqrt(k1*k2*c1.center*c2.center+k1*k3*c1.center*c3.center+k2*k3*c2.center*c3.center))/k)
        C = circle(cent1,abs(1/k))
        cent2 = ((c1.center*k1+c2.center*k2+c3.center*k3-
                     2*np.sqrt(k1*k2*c1.center*c2.center+k1*k3*c1.center*c3.center+k2*k3*c2.center*c3.center))/k)
        c = circle(cent2,np.abs(1/k))
        # check tangency. Both may be tangent 

        if (isTangent(c1,c) & isTangent(c2,c) & isTangent(c3,c)):
            clist.append(c)
        if(isTangent(c1,C) & isTangent(c2,C) & isTangent(c3,C)):
            clist.append(C)
        
        # return only the first two elements of clist --- if both curvatures are equal, 
        # there will be 4 circles
    return clist[0], clist[1]
        
# given three circles and a number of iterations, create the corresponding gasket
def makeGasket(c1,c2,c3,n):
    # check that the circles are mutually tangent
    if not(isTangent(c1,c2) & isTangent(c2,c3) & isTangent(c3,c1)): 
        return None
    
    # initialize the gasket
    gasket = [c1,c2,c3]
    centerlist = [] # keep track of centers
    for k in range(0,len(gasket)):
        gasket[k].generation = 0
        gasket[k].firstTangencies = [gasket[(k-1) %3], gasket[(k+1) %3]]
        centerlist.append(gasket[k].center)
 
    # there are fewer initial tangencies in the first generation. Iterate once to fix that
    if n > 0:
        newCircles = descarte(c1,c2,c3)
        for k in range(0,len(newCircles)):
            newCircles[k].generation = 1
            newCircles[k].firstTangencies = [c1,c2,c3]
            centerlist.append(newCircles[k].center)
            gasket.append(newCircles[k])
    # now increment generations
    genInd = [3,len(gasket)] # indices for when the previous generation starts / ends in the list
    gen = 2
    while gen < n:
        # find all circles which are from the last generation

        for k in range(genInd[0],len(gasket)):
            circleCandidates = []
            circleCandidates.extend(descarte(gasket[k],gasket[k].firstTangencies[1],
                                        gasket[k].firstTangencies[2]))
            circleCandidates.extend(descarte(gasket[k].firstTangencies[0],gasket[k],
                                        gasket[k].firstTangencies[2]))
            circleCandidates.extend(descarte(gasket[k].firstTangencies[0],gasket[k].firstTangencies[1],
                                        gasket[k]))
            
            for j in range(0,len(circleCandidates)):
                # we determine a repeated circle by using the centers
                circ = circleCandidates[j]
                if not any(np.isclose(circ.center,centerlist)):
                    circ.generation = gen
                    # the first tangencies are determined by when the circle was added to candidates
                    if j in {0,1}:
                        circ.firstTangencies = [gasket[k],gasket[k].firstTangencies[1],
                                        gasket[k].firstTangencies[2]]
                    elif j in {2,3}:
                        circ.firstTangencies = [gasket[k].firstTangencies[0],gasket[k],
                                        gasket[k].firstTangencies[2]]
                    elif j in {4,5}:
                        circ.firstTangencies = [gasket[k].firstTangencies[0],gasket[k].firstTangencies[1],
                                        gasket[k]]
                    gasket.append(circ)
                    centerlist.append(circ.center)

        gen += 1
        genInd = [genInd[1], len(gasket)]
    return gasket

# find the largest circle in a gasket. 
# Assumes there is a single biggest circle containing the others
def findBiggestCircle(gasket):
    maxrad = 0
    
    for k, c in enumerate(gasket):
        if c.radius > maxrad:
            biggestCirc = c
            maxrad = c.radius
    return biggestCirc 

def plotGasket(gasket,noColors= False,axis = None,normalize = None,animated = False):
    if axis is None:
        fig, ax  = plt.subplots()
    else: 
        ax = axis
        fig = None

    ax.clear() # clear current axis
    t = np.linspace(0, 2*np.pi, 100)

    # Extract generation values (or set to None)
    generations = [c.generation if hasattr(c, 'generation') and c.generation is not None else None for c in gasket]
    gen_vals = [c for c in generations if c is not None]

    use_colors = len(gen_vals) > 0 and not noColors

    if normalize: # normalize each circle in the gasket
        normgasket = gasket
        bcirc = findBiggestCircle(gasket)
        bcent = bcirc.center
        brad = bcirc.radius

        for c in normgasket:
            c.center = (c.center - bcent)/brad
            c.radius = c.radius/brad

    if use_colors:
        # Normalize generation values
        gen_min = min(gen_vals)
        gen_max = max(gen_vals)
        norm = plt.Normalize(vmin=gen_min, vmax=gen_max)
        cmap = plt.cm.nipy_spectral

    if not normalize:
        for k, c in enumerate(gasket):
            z = c.center + c.radius * np.exp(1j * t)
            x, y = z.real, z.imag

            if generations[k] is not None and use_colors:
                color = cmap(norm(generations[k]))
            else:
                color = 'black'
            ax.plot(x, y, color=color)
    else: # in case the gasket is normalized
        for k, c in enumerate(normgasket):
            z = c.center + c.radius * np.exp(1j * t)
            x, y = z.real, z.imag

            if generations[k] is not None and use_colors:
                color = cmap(norm(generations[k]))
            else:
                color = 'black'
            ax.plot(x, y, color=color)
    if axis is None:
        return fig, ax
    else:
        return None