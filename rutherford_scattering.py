from visual import *
from visual.graph import *

k = 9.0e9
proton_charge = 1.6e-19
proton_mass = 1.67e-27
rgold = 0.5 * 3.3e-14 # Actual radius 7.3e-15
size = 20.0 * rgold

scene = display(title = 'Rutherford Scattering', width = 800, height = 600, range = size)
scene.autoscale = 0

gold = sphere(pos = vector(0, 0, 0), radius = rgold, color = color.yellow,
              mass = (79.0 + 118.0) * proton_mass, charge = 79.0 * proton_charge,
              momentum = vector())

impact_parameter = rgold * 0.175

alpha = sphere(pos = vector(-0.9 * size, impact_parameter, 0), radius = 0.5 * rgold, color = color.red,
               mass = 4.0 * proton_mass, charge = 2.0 * proton_charge, energy = 1e7)

# Non-relativistic calculation of particle speed
alpha.speed = pow(2.0 * (alpha.energy * proton_charge) / alpha.mass, 0.5)
print(alpha.speed)
alpha.momentum = alpha.mass * vector(alpha.speed, 0, 0)
trailalpha = curve(pos = alpha.pos, color = alpha.color)

dt = rgold / alpha.speed / 8
t = 0
exit = False
while not exit:

    f = vector()
    if mag(alpha.pos - gold.pos) >= rgold:
        f = norm(alpha.pos - gold.pos) * k * alpha.charge * gold.charge / mag2(gold.pos - alpha.pos)
    else :
        f = (alpha.pos - gold.pos) * k * alpha.charge * gold.charge / pow(rgold, 3.0)

    #  Update the alpha momentum and position.
    alpha.momentum += f * dt
    alpha.pos += alpha.momentum * dt / alpha.mass
    trailalpha.append(pos = alpha.pos)

    # Put code here for when you include the recoil of the gold nucleus.
    gold.momentum += -f * dt
    gold.pos += gold.momentum * dt / gold.mass

    # Exit the loop if the alpha is more than 1.5 times the screen size from the origin.
    t += dt
    if mag(alpha.pos) > (1.5 * size) or t > 1:
        exit = True
    rate(100)

# Put code here to calculate the scattering angle of the alpha and 
# print it out in degrees, along with the value of the impact parameter.
theta = diff_angle(vector(1, 0, 0), alpha.momentum)
scattering_angle = degrees(theta)
print(impact_parameter, scattering_angle)
