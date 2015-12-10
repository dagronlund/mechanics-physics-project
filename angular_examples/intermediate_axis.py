import sys
sys.path.append("..")

import numpy as np
from visual import *
from math_utils import *
from physics_utils import *

def orient_box(box, axis, sys):
    box.axis = mtov(sys[:,0]) * box.size.x
    box.up = mtov(sys[:,1]) * box.size.y
    axis.axis = mtov(sys[:,1]) * box.size.y / 2.0

display(width = 800, height = 600)

dt = 0.005
sys = np.matrix(np.identity(3))
omega_p = vector(.01, 1, 0)

b = box(size = (10, 6, 2), color = color.red, mass = 5, opacity = 0.5)
axes = box_principal_axes(b.mass, b.size.x, b.size.y, b.size.z)

omega_axis = arrow(pos = vector(-8, -8, -8), shaftwidth = 0, 
    color = color.yellow, opacity = 1)
l_axis = arrow(pos = vector(-8, -10, -8), shaftwidth = 0, 
    color = color.green, opacity = 1)
box_axis = arrow(color = color.orange, shaftwidth = 0)

while True:

    # Convert omega-prime to omega
    omega = (sys.I * omega_p.mat()).vec()

    # Update omega from Euler's equations
    torque = vector()
    omega += delta_omega(axes, omega, torque) * dt
    
    # Calculate l-prime from omega and compensate angular velocity
    l = (sys * (inertia_tensor(axes) * omega.mat())).vec()
    
    # Convert omega back to omega-prime
    omega_p = (sys * omega.mat()).vec()

    # Rotate coordinate system by omega-prime
    sys = sys.rotate(omega_p * dt)

    # Rotate object to match coordinate system
    orient_box(b, box_axis, sys)

    # Update diagnostics
    omega_axis.axis = norm(omega_p) * 3
    l_axis.axis = norm(l) * 3

    rate(300)
