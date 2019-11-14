import pulp
import numpy as np
import random
import matplotlib.pyplot as plt

def nsphere_to_cartesian(r, arr):
    a = np.concatenate((np.array([2*np.pi]), arr))
    si = np.sin(a)
    si[0] = 1
    si = np.cumprod(si)
    co = np.cos(a)
    co = np.roll(co, -1)
    return si*co*r

# n is the number of columns
# square by default
# the objective coefficients being between 0, and 10
# , or the probability of the variable being integer
# (50%), or the valid point being between 0 and 50
# is entirely arbitrary
def GenRandMIP(n, m, filename):

    prob = pulp.LpProblem(filename, pulp.LpMaximize)

    option = [0,1]
    binary_choice = [random.choice(option) for a in range(n)]
    obj_coefs = [random.uniform(0.0, 10.0) for a in range(n)]
    x = [0 for a in range(n)]
    for i in range(n):
        if(binary_choice[i]):
            x[i] = pulp.LpVariable('x' + str(i), lowBound=0, cat='Integer')
        else:
            x[i] = pulp.LpVariable('x' + str(i), lowBound=0)

    prob += sum([obj_coefs[i]*x[i] for i in range(n)])

    # Get the H-representation of a polytope in n-dimensions with m points.
    A, b = RandPolytope(n, m)

    for j,a in enumerate(A):
        prob += sum([a[i]*x[i] for i in range(n)]) <= np.abs(b[j])

    prob.writeLP(filename + ".lp")


def RandPolytope(n, m):
    import scipy.spatial as sp


    # Hyperspheroid coordinates take the form
    # x_1 = r*cos(t_1)
    # x_2 = r*sin(t_1)*cos(t_2)
    # x_3 = r*sin(t_1)*sin(t_2)*cos(t_3)
    # ...
    # x_n = r*sin(t_1)*...*sin(t_n-1)*cos(t_n)
    r = random.uniform(1.0, 10.0)
    arr = []
    for i in range(m):
        angles = [np.deg2rad(random.randint(1,360)) for a in range(n-1)]
        #arr.append(nsphere_to_cartesian(r,angles))
        arr.append([random.uniform(0.0,50.0) for a in range(n)])


    # For now we just have the point (0) as our guaranteed point
    arr.append(np.array([0 for a in range(n)]))
    hull = sp.ConvexHull(arr)

    A = hull.equations[:,0:-1]
    b = hull.equations[:,-1]

    return A, b

GenRandMIP(2,5, 'test2')
