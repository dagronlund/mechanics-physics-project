import sys
sys.path.append("..")

import numpy as np
from visual import *
from math_utils import *
from physics_utils import *

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
omega_p = uy * 20

sys = sys.rotate(theta * -uz)
omega_p = omega_p.rotate(theta, -uz)

top = cylinder(radius = 5, height = 0.5, mass = 5)
top_axis = cylinder(radius = 0.25, height = 10)
top_direction = cylinder(radius = 0.27, height = 11, color = color.red)
top_trail = curve(color = color.red)
axes = cylinder_principal_axes(top.mass, 2.5, 5)

# Optional code to provide initial angular velocity to cancel out nutations
omega_precession = top.mass * 9.8 * (top_axis.height / 2) / (axes[1] * mag(omega_p)) * uy
# omega_p += omega_precession

arrow_offset = vector(-12, 0, 0)
omega_axis = arrow(pos = arrow_offset + uy * 4, shaftwidth = 0, 
    color = color.yellow, opacity = 1)
l_axis = arrow(pos = arrow_offset, shaftwidth = 0, 
    color = color.green, opacity = 1)
torque_axis = arrow(pos = arrow_offset - uy * 4, color = color.orange)

while True:

    # Convert omega-prime to omega
    omega = (sys.I * omega_p.mat()).vec()

    # Calculate torque in world-space
    r = -sys[:,1] * top_axis.height / 2.0
    fg = top.mass * 9.8 * uy
    torque_p = cross(r, fg)

    # Convert torque to body-space
    torque = (sys.I * torque_p.mat()).vec()

    # Update omega from Euler's equations
    omega += delta_omega(axes, omega, torque) * dt
    
    # Calculate l-prime from omega and compensate angular velocity
    l = (sys * (inertia_tensor(axes) * omega.mat())).vec()
    
    # Convert omega back to omega-prime
    omega_p = (sys * omega.mat()).vec()

    # Rotate coordinate system by omega-prime
    sys = sys.rotate(omega_p * dt)

    # Rotate object to match coordinate system
    orient_top(top, top_axis, top_direction, top_trail, sys)

    # Update diagnostics
    omega_axis.axis = omega_p / 4.0
    l_axis.axis = l / 60.0
    torque_axis.axis = torque_p / 20.0

    rate(200)
