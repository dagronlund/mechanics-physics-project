from visual import *
import numpy as np
import numpy.linalg as npl
from math_utils import *
from physics_utils import *
from time import time

# def orient_box(box, sys):
#     box.axis = mtov(sys[:,0]) * box.size.x
#     box.up = mtov(sys[:,1]) * box.size.y

# Moves top around in world-space to fix the bottom of the top
def orient_top(top_body, top_axis, top_direction, top_trail, sys):
    offset = -sys[:,1] * top_axis.height / 2.0
    
    top_body.pos = -sys[:,1] * top_body.height / 2.0 - offset
    top_axis.pos = -sys[:,1] * top_axis.height / 2.0 - offset
    top_direction.pos = -sys[:,2] * top_direction.height / 2.0 - offset

    top_axis.axis = sys[:,1] * top_axis.height
    top_body.axis = sys[:,1] * top_body.height
    top_direction.axis = sys[:,2] * top_direction.height

    top_trail.append(pos = -offset * 2)

display(width = 800, height = 600)

theta = pi / 12.0
dt = 0.002
sys = np.matrix(np.identity(3))
omega_p = uy * 12

sys = sys.rotate(theta * -uz)
omega_p = omega_p.rotate(theta, -uz)

# b = box(size = (10, 6, 2), color = color.red, mass = 5, opacity = 0.5)
# axes = box_principal_axes(b.mass, b.size.x, b.size.y, b.size.z)

top = cylinder(radius = 5, height = 0.5, mass = 5)
top_axis = cylinder(radius = 0.25, height = 10)
top_direction = cylinder(radius = 0.27, height = 11, color = color.red)
top_trail = curve(color = color.red)
axes = cylinder_principal_axes(top.mass, 2.5, 5)

# Optional code to provide initial angular velocity to cancel out nutations
omega_precession = top.mass * 9.8 * (top_axis.height / 2) / (axes[1] * mag(omega_p)) * uy
omega_p += omega_precession

arrow_offset = vector(-12, 0, 0)
omega_axis = arrow(pos = arrow_offset + uy * 4, shaftwidth = 0, 
    color = color.yellow, opacity = 1)
l_axis = arrow(pos = arrow_offset, shaftwidth = 0, 
    color = color.green, opacity = 1)
torque_axis = arrow(pos = arrow_offset - uy * 4, color = color.orange)

while True:
    
    # start = time() * 1000.0

    # # Run update loop fives times before drawing
    # for i in range(0, 1):

    # Convert omega-prime to omega
    omega = (sys.I * omega_p.mat()).vec()
    
    # Find acceleration of tip in z-axis
    # ...

    # Calculate torque in world-space
    r = -sys[:,1] * top_axis.height / 2.0
    fg = top.mass * 9.8 * uy
    torque_p = cross(r, fg)

    # Convert torque to body-space
    torque = (sys.I * torque_p.mat()).vec()
    # torque = vector()

    # Update omega from Euler's equations
    omega += delta_omega(axes, omega, torque) * dt
    
    # Calculate l-prime from omega and compensate angular velocity
    l = (sys * (inertia_tensor(axes) * omega.mat())).vec()
    
    # Convert omega back to omega-prime
    omega_p = (sys * omega.mat()).vec()

    # Rotate coordinate system by omega-prime
    sys = sys.rotate(omega_p * dt)

    # Rotate object to match coordinate system
    # orient_box(b, sys)
    # orient_rods(parts, sys)
    # orient_cone(top, sys)
    # point.pos = -r * 2
    orient_top(top, top_axis, top_direction, top_trail, sys)

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
    torque_axis.axis = torque_p / 20.0

    #stop = time() * 1000.0
    #print(stop - start)

    rate(200)

    # omega /= mag(l) / mag(conserved_momentum)
    # print("L: ", mtov(np.dot(sys, mtov(np.dot(inertia_tensor(axes), omega)))).mag)
    # torque = cone_torque(-sys[:,1], m * vector(0, -9.8, 0), top.height)
    # torque = vector()

