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
    #obj_coefs = [random.uniform(0.0, 10.0) for a in range(n)]
    obj_coefs = [1 for a in range(n)]
    x = [0 for a in range(n)]
    for i in range(n):
        if(binary_choice[i]):
            x[i] = pulp.LpVariable('x' + str(i), cat='Integer')
        else:
            x[i] = pulp.LpVariable('x' + str(i))

    prob += sum([obj_coefs[i]*x[i] for i in range(n)])

    # The 0 vector is the guaranteed point
    r = [0 for a in range(n)]
    # Get the H-representation of a polytope in n-dimensions with m points.
    A, b = RandPolytope(n, m)
    #A, b = So(n,m)
    print(A)
    print(b)

    for j,a in enumerate(A):
        #if (sum([a[i]*r[i] for i in range(n)]) <= b[j]):
        #    prob += pulp.lpSum([a[i]*x[i] for i in range(n)]) >= b[j]
        #else:
        #    prob += pulp.lpSum([a[i]*x[i] for i in range(n)]) <= b[j]
        prob += pulp.lpSum([a[i]*x[i] for i in range(n)]) <= -b[j]

    prob.writeLP(filename + ".lp")

def RandPolytope(n, m):
    import scipy.spatial as sp

    # Hyperspheroid coordinates take the form
    # x_1 = r*cos(t_1)
    # x_2 = r*sin(t_1)*cos(t_2)
    # x_3 = r*sin(t_1)*sin(t_2)*cos(t_3)
    # ...
    # x_n = r*sin(t_1)*...*sin(t_n-1)*cos(t_n)
    r = random.uniform(1.0, 1000.0)
    arr = []
    for i in range(m):
        angles = [np.deg2rad(random.randint(1,360)) for a in range(n-1)]
        arr.append(nsphere_to_cartesian(r,angles))
        #arr.append([random.uniform(0.0,50.0) for a in range(n)])

    # For now we just have the point (0) as our guaranteed point
    arr.append(np.array([0 for a in range(n)]))
    hull = sp.ConvexHull(arr)

    A = hull.equations[:,0:-1]
    b = hull.equations[:,-1]

    return A, b

def RandConst(n,m, a=-50,b=50):
    # This vector is our guaranteed solution
    v = np.matrix([random.uniform(a,b) for i in range(n)])

    # Random matrix n elements wide, and m tall
    A = np.random.rand(m,n)

    #delta = np.matrix([random.uniform(a/10.0,b/10.0) for i in range(m)])
    b = A*v.T

    return A,b

def So(n,m):
    A = np.random.randn(m,n)
    A[0,:] = np.random.randn(n) + 0.1
    b = np.dot(A, np.random.randn(n) + 0.01)

    return A, b

def RandReject(n,m):
    p = [0 for i in range(n)]
    A = []
    b = []
    for i in range(int(m/2)):
        bs = False
        while (not bs):
            b_i = random.uniform(-50.0,50.0)
            A_i = [random.uniform(-50.0/b_i,0) for j in range(n)]
            if (sum([A_i[j]*p[j] for j in range(n)]) <= b_i):
                bs = True
                A.append(A_i)
                b.append(b_i)

    for i in range(int(m/2),m):
        bs = False
        while (not bs):
            b_i = random.uniform(-50.0, 50.0)
            A_i = [random.uniform(0.0,50.0/b_i) for j in range(n)]
            if (sum([A_i[j]*p[j] for j in range(n)]) <= b_i):
                bs = True
                A.append(A_i)
                b.append(b_i)

    return A, b

#GenRandMIP(2,4, 'test2')

def bs(x):
    if x < 10:
        return "0" + str(x)
    else:
        return str(x)

for i in range(2,15):
    for j in range(0,10):
        filename = bs(j) + "dim_test" + bs(i)
        GenRandMIP(i,i+2, filename)
