import matplotlib.pyplot as plt
import numpy as np

class Circle:
    def __init__(self, x, y, r):
        self.x = x  # center x
        self.y = y  # center y
        self.r = r  # radius
        self.k = 1/r  # curvature

    def plot(self, ax, **kwargs):
        circle = plt.Circle((self.x, self.y), self.r, fill=False, **kwargs)
        ax.add_patch(circle)

def descartes(c1, c2, c3):
    # Solve for the fourth curvature
    k1, k2, k3 = c1.k, c2.k, c3.k
    k4_pos = k1 + k2 + k3 + 2*np.sqrt(k1*k2 + k2*k3 + k3*k1)
    k4_neg = k1 + k2 + k3 - 2*np.sqrt(k1*k2 + k2*k3 + k3*k1)

    return k4_pos, k4_neg

def solve_circle(c1, c2, c3, k4):
    # Based on complex Descartes formula for positions
    z1 = complex(c1.x, c1.y)
    z2 = complex(c2.x, c2.y)
    z3 = complex(c3.x, c3.y)
    k1, k2, k3 = c1.k, c2.k, c3.k

    z4 = (k1*z1 + k2*z2 + k3*z3 + 2*np.sqrt(k1*k2*(z1 - z2)**2 + 
                                            k2*k3*(z2 - z3)**2 + 
                                            k3*k1*(z3 - z1)**2)) / k4
    return Circle(z4.real, z4.imag, 1/k4)

def recurse(c1, c2, c3, depth, seen, ax):
    if depth == 0:
        return

    k4a, k4b = descartes(c1, c2, c3)
    for k4 in [k4a, k4b]:
        c4 = solve_circle(c1, c2, c3, k4)
        key = tuple(sorted([round(ci.k, 6) for ci in [c1, c2, c3, c4]]))
        if key in seen:  # avoid duplicates
            continue
        seen.add(key)
        c4.plot(ax, color='black', linewidth=0.5)
        recurse(c1, c2, c4, depth-1, seen, ax)
        recurse(c1, c3, c4, depth-1, seen, ax)
        recurse(c2, c3, c4, depth-1, seen, ax)

def main():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    # Outer bounding circle and three inner mutually tangent circles
    R = 1.0
    c0 = Circle(0, 0, R)  # outer circle
    c1 = Circle(-1/3, 0, 1/3)
    c2 = Circle(1/3, 0, 1/3)
    c3 = Circle(0, np.sqrt(3)/3, 1/3)

    c0.plot(ax, color='black', linewidth=1.5)
    for c in [c1, c2, c3]:
        c.plot(ax, color='black', linewidth=0.5)

    seen = set()
    recurse(c1, c2, c3, depth=6, seen=seen, ax=ax)

    plt.show()

if __name__ == "__main__":
    main()
