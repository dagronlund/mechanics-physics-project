import sys
sys.path.append("..")

import numpy as np
from visual import *
from math_utils import *
from physics_utils import *

def orient_top(top_body, top_axis, top_direction, sys):
    top_body.pos = -sys[:,1] * top_body.height / 2.0
    top_body.axis = sys[:,1] * top_body.height
    top_axis.pos = -sys[:,1] * top_axis.height / 2.0
    top_axis.axis = sys[:,1] * top_axis.height
    top_direction.pos = -sys[:,2] * top_direction.height / 2.0
    top_direction.axis = sys[:,2] * top_direction.height

display(width = 800, height = 600)

dt = 0.005
sys = np.matrix(np.identity(3)).rotate(vector(0, 0, -1) * pi / 12.0)
omega_p = vector(0, 1, 0)

top = cylinder(radius = 5, height = 0.5, mass = 5)
top_axis = cylinder(radius = 0.25, height = 10)
top_direction = cylinder(radius = 0.27, height = 11, color = color.red)

axes = cylinder_principal_axes(top.mass, 2.5, 5)

omega_axis = arrow(pos = vector(-8, -8, -8), shaftwidth = 0, 
    color = color.yellow, opacity = 1)
l_axis = arrow(pos = vector(-8, -10, -8), shaftwidth = 0, 
    color = color.green, opacity = 1)

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
    orient_top(top, top_axis, top_direction, sys)

    # Update diagnostics
    omega_axis.axis = norm(omega_p) * 3
    l_axis.axis = norm(l) * 3

    rate(300)