from visual import *
from visual.graph import *
from physics_utils import *

year  = 365.25 * 24.0 * 3600.0     
max_t = 2.0 * year                  
dt = 5000
t = 0

display(title = 'Planetary Orbit', width = 600, height = 600, range = 3e11)
gdisplay( title = 'L vs. t', xtitle = 't (s)',
          ytitle = 'L (scaled)', xmax = max_t, ymax = 10.0,
          x = 0, y = 600, width = 500, height = 300)
l_curve = gcurve(color = color.yellow)
rl_curve = gcurve(color = color.green)
scene.autoscale = 0

sun_mass = 1.989e30
sun_radius = 6.963e8
sun_scale = 1e1

earth_mass = 5.972e24
earth_distance = 1.496e11
earth_radius = 6.371e6
earth_scale = 1e3

sun = sphere(pos = vector(), color = color.yellow,
    mass = sun_mass, radius = sun_radius * sun_scale)
earth = sphere(pos = vector(earth_distance, 0, 0), color = color.cyan, make_trail = True,
    mass = earth_mass, radius = earth_radius * earth_scale,
    momentum = earth_mass * vector(0, 2 * pi * earth_distance / year, 0) * 1.1)

f_arrow = arrow(shaft = 1e6, color = color.red)
p_arrow = arrow(shaft = 1e6, color = color.green)
l_arrow = arrow(shaft = 1e6, color = color.magenta)
rl_arrow = arrow(shaft = 1e6, color = color.yellow)

while t < max_t:

    # Update momentum and position
    f = earth.fg(sun)
    earth.momentum += f * dt
    earth.move(earth.v() * dt)

    # Calculate the angular momentum and Runge-Lenz vectors here.
    l_origin = vector(3.0 * earth_distance / 2.0, 0, 0)
    l_origin = vector()
    l = earth.l(l_origin)
    rl = earth.rl(sun)

    l_curve.plot(pos = (t, mag(l) / 5e39))

    p_arrow = f_arrow.pos = earth.pos
    l_arrow.pos = l_origin
    p_arrow.axis = earth.momentum / 5e18
    f_arrow.axis = f / 1e12
    l_arrow.axis = l / 5e29
    rl_arrow.axis = rl / 5e57

    t += dt
    rate(1000)

print "Orbit program has finished"
