from visual import *
import numpy as np
import numpy.linalg as npl
from math_utils import *
from physics_utils import *
from time import time

def orient_box(box, sys):
    box.axis = mtov(sys[:,0]) * box.size.x
    box.up = mtov(sys[:,1]) * box.size.y

def orient_rods(rods, sys):
    for rod in rods:
        rod.pos = mtov(np.dot(sys, rod.p))
        rod.axis = mtov(np.dot(sys, rod.a))

def orient_cone(cone, sys):
    cone.pos = sys[:,1] * cone.height / 4.0
    cone.axis = -sys[:,1] * cone.height

display(width = 800, height = 600)

theta = pi / 6.0
dt = 0.005
sys = np.matrix(np.identity(3))
omega_p = vector(.05, 1, .05)
# sys = np.matrix(np.identity(3)).rotate(vector(0, 0, -1) * theta)
# omega_p = vector(0, 60, 0).rotate(theta, vector(0, 0, -1))


b = box(size = (10, 6, 2), color = color.red, mass = 5, opacity = 0.5)
axes = box_principal_axes(b.mass, b.size.x, b.size.y, b.size.z)

# top = cone(radius = 2.5, height = 5, mass = 5, color = color.red, opacity = 0.5)
# point = sphere(radius = 0.5, color = color.red, make_trail = True)
# axes = cone_principal_axes(top.mass, 2.5, 5)

omega_axis = arrow(pos = vector(-8, -8, -8), shaftwidth = 0, 
    color = color.yellow, opacity = 1)
l_axis = arrow(pos = vector(-8, -10, -8), shaftwidth = 0, 
    color = color.green, opacity = 1)
# box_axis = arrow(color = color.orange, shaftwidth = 0)
# cone_axis = arrow(color = color.orange, shaftwidth = 0, make_trail = True)
# x_axis = arrow(color = color.magenta)
# y_axis = arrow(color = color.yellow)
# z_axis = arrow(color = color.cyan)
# r_axis = arrow(color = color.yellow)
# fg_axis = arrow(color = color.red)
torque_axis = arrow(color = color.green)

print(axes)

# conserved_momentum = mtov(np.dot(sys, mtov(np.dot(inertia_tensor(axes), mtov(np.dot(sys.I, omega_p))))))
conserved_momentum = (sys * (inertia_tensor(axes) * (sys.I * omega_p.mat()))).vec()
print(conserved_momentum)

while True:
    
    start = time() * 1000.0

    # Run update loop fives times before drawing
    for i in range(0, 1):

        # Convert omega-prime to omega
        omega = (sys.I * omega_p.mat()).vec()
        
        # Find acceleration of tip in z-axis
        # ...

        # Calculate torque in world-space
        # r = -sys[:,1] * (3.0 / 4.0) * top.height
        # fg = top.mass * vector(0, -9.8, 0)
        # torque = cross(r, fg)

        # Convert torque to body-space
        # torque = (sys.I * torque.mat()).vec()
        torque = vector()

        # Update omega from Euler's equations
        omega += delta_omega(axes, omega, torque) * dt
        
        # Calculate l-prime from omega and compensate angular velocity
        l = (sys * (inertia_tensor(axes) * omega.mat())).vec()
        
        # Convert omega back to omega-prime
        omega_p = (sys * omega.mat()).vec()

        # Rotate coordinate system by omega-prime
        sys = sys.rotate(omega_p * dt)

    # Rotate object to match coordinate system
    orient_box(b, sys)
    # orient_rods(parts, sys)
    # orient_cone(top, sys)
    # point.pos = -r * 2

    # Update diagnostics
    omega_axis.axis = norm(omega_p) * 3
    l_axis.axis = norm(l) * 3
    # cone_axis.pos = -top.axis * 0.75
    # cone_axis.axis = top.axis * 0.75
    # box_axis.axis = mtov(sys[:,0]) * b.size.x / 2.0
    # x_axis.axis = mtov(sys[:,0])
    # y_axis.axis = mtov(sys[:,1])
    # z_axis.axis = mtov(sys[:,2])
    # print(l.mag)
    # r_axis.axis = r
    # fg_axis.pos = r
    # fg_axis.axis = fg / 20
    # torque_axis.axis = norm(cross(r, fg)) * 5

    stop = time() * 1000.0
    print(stop - start)

    rate(300)

    # omega /= mag(l) / mag(conserved_momentum)
    # print("L: ", mtov(np.dot(sys, mtov(np.dot(inertia_tensor(axes), omega)))).mag)
    # torque = cone_torque(-sys[:,1], m * vector(0, -9.8, 0), top.height)
    # torque = vector()