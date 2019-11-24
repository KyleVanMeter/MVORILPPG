#
# Visualize the feasible region of 2d polytopes
#
import numpy as np
import random
import matplotlib.pyplot as plt
import functools

def RandConst(n,m, a=-50,b=50):
    # This vector is our guaranteed solution
    v = np.matrix([random.uniform(a,b) for i in range(n)])

    # Random matrix n elements wide, and m tall
    A = np.random.rand(m,n)

    #delta = np.matrix([random.uniform(a/10.0,b/10.0) for i in range(m)])
    b = A*v.T

    return A.tolist(),b.tolist()

def nsphere_to_cartesian(r, arr):
    a = np.concatenate((np.array([2*np.pi]), arr))
    si = np.sin(a)
    si[0] = 1
    si = np.cumprod(si)
    co = np.cos(a)
    co = np.roll(co, -1)
    return si*co*r

def RandPolytope(n, m):
    import scipy.spatial as sp

    # Hyperspheroid coordinates take the form
    # x_1 = r*cos(t_1)
    # x_2 = r*sin(t_1)*cos(t_2)
    # x_3 = r*sin(t_1)*sin(t_2)*cos(t_3)
    # ...
    # x_n-1 = r*sin(t_1)*...*sin(t_n-1)*cos(t_n)
    # x_n = r*sin(t_1)*...*sin(t_n-1)*sin(t_n)
    r = random.uniform(1.0, 100.0)
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

# plot the feasible region
d = np.linspace(-200,200,3000)
x,y = np.meshgrid(d,d)
#coef1 = [[-1,0],[2,1],[-4,2],[1,-2]]
#coef2 = [-2,25,8,-5]
coef1, coef2 = RandConst(2,4)
print(coef1)
print(coef2)
A = [[coef1[i][0]*y+coef1[i][1]*x <= coef2[i]] for i in range(len(coef2))]
#A = [[-1*y+0*x<=-2],[2*y+1*x<=25],[-4*y+2*x<=8],[1*y-2*x<=-5]]
#plt.imshow( ((y>=2) & (2*y<=25-x) & (4*y>=2*x-8) & (y<=2*x-5)).astype(int) , 
#                extent=(x.min(),x.max(),y.min(),y.max()),origin="lower", cmap="Greys", alpha = 0.3);
#plt.imshow( ((A[0][0]) & (A[1][0]) & (A[2][0]) & (A[3][0])).astype(int) , 
#                extent=(x.min(),x.max(),y.min(),y.max()),origin="lower", cmap="Greys", alpha = 0.3);
plt.imshow( (functools.reduce(lambda a,b: a & b, [A[i][0] for i in range(len(A))])).astype(int), extent=(y.min(),y.max(),x.min(),x.max()),origin="lower", cmap="Greys", alpha = 0.3);

# plot the lines defining the constraints
x = np.linspace(-200, 200, 20000)
# y >= 2
#y1 = (x*0) + 2
#y1 = (-1*coef1[0][1]*x + coef2[0]) / coef1[0][0]
# 2y <= 25 - x
#y2 = (25-x)/2.0
#y2 = (-1*coef1[1][1]*x + coef2[1]) / coef1[1][0]
# 4y >= 2x - 8 
#y3 = (2*x-8)/4.0
# 2*x+4*y <= 8
#y3 = (-1*coef1[2][1]*x + coef2[2]) / coef1[2][0]
# y <= 2x - 5 
#y4 = 2 * x -5
# -2*x+1*y <= -5
#y4 = (-1*coef1[3][1]*x + coef2[3]) / coef1[3][0]

for i in range(len(coef1)):
    plt.plot(x, (-1*coef1[i][1]*x + coef2[i]) / coef1[i][0])

# Make plot
#plt.plot(x, 2*np.ones_like(y1))
#plt.plot(x, y1)
#plt.plot(x, y2, label=r'$2y\leq25-x$')
#plt.plot(x, y3, label=r'$4y\geq 2x - 8$')
#plt.plot(x, y4, label=r'$y\leq 2x-5$')
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.ylim(-200,200)
plt.grid()
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.show()
