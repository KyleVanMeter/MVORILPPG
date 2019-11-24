from coinor.grumpy.polyhedron2D import Polyhedron2D, Figure

def RandPolytope(n, m):
    import scipy.spatial as sp
    import random
    import numpy as np

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

    #return A, b
    return hull.points

#points = [[2.5, 4.5], [6.5, 0.5], [0.5, 1],
#          [7, 5.7], [7.7, 5], [2, 0.25]]
points = RandPolytope(2,9)
rays = []
c = [2, 5]
opt = [7, 5.7]
loc = (opt[0]+0.1, opt[1]-0.1)
obj_val = 42.5

p = Polyhedron2D(points = points, rays = rays)
f = Figure()
f.add_polyhedron(p, label = 'Polyhedron $P$', color = 'red')
f.set_xlim([p.xlim[0], p.xlim[1]+1])
f.set_ylim([p.ylim[0], p.ylim[1]+2])
f.add_line(c, obj_val, p.xlim + [0.2, 0.8], p.ylim + [0.2, 1.8], 
           linestyle = 'dashed', color = 'black', label = "Objective Function")
f.add_point(opt, 0.04, 'red')
f.add_text(loc, r'$x^* = %s$' % str(opt))
f.show()
