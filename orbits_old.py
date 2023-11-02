from matplotlib import pyplot as plt
import matplotlib.animation
import numpy as np
from icecream import ic

# Assign global variables, time interval and bigG#
bigG = 10000
dt = 0.01
density = 1

# Assign starting points
planetData = np.zeros(3, dtype= [('position', float, (2,)),
                                ('velocity', float, (2,)),
                                ('mass', float, (1,)),
                                ('radius', float, (1,))])
planetData['position'] = np.array([[50, 75],
                       [-30, 15],
                       [0, -10]])
planetData['velocity'] = np.array([[-10, -20],
                       [1, -2],
                       [0, 0]])
planetData['mass'] = np.array([[1], [2], [3]])

# planetData = np.zeros(2, dtype= [('position', float, (2,)),
#                                 ('velocity', float, (2,)),
#                                 ('mass', float, (1,)),
#                                 ('radius', float, (1,))])
# planetData['position'] = np.array([[47, 70],
#                        [-16.8669, 5.66]])
# planetData['velocity'] = np.array([[-3.12, -4.3287],
#                        [51.35, 52.68]])
# planetData['mass'] = np.array([[1], [6]])



# Calculated starting points
planetData['radius'] = np.cbrt(planetData['mass'] / density)
smallestRadius = np.min(planetData['radius'])

# Scatter plot setup
fig, ax = plt.subplots()
plt.xlim(-100,100)
plt.ylim(-100,100)
sizeMulti = 100
sc = ax.scatter(x = planetData['position'][:, 0], y= planetData['position'][:, 1], c= planetData['mass'], s= planetData['radius']*sizeMulti)

def modelPlanetMerges(pData):
    toggle = False
    startPlanets = len(pData)
    xdist = np.tile(pData['position'][:, 0], (startPlanets,1))
    xdist -= np.transpose(xdist)
    ydist = np.tile(pData['position'][:, 1], (startPlanets,1))
    ydist -= np.transpose(ydist)
    totalDistSqrd = xdist * xdist + ydist * ydist
    # Make zero distances non-zero to avoid div0 errors
    totalDistSqrd += (totalDistSqrd == 0) * smallestRadius
    totalDist = np.sqrt(totalDistSqrd)
    collisionRadius = np.tile(pData['radius'].flatten(), (startPlanets,1))
    collisionRadius += np.transpose(collisionRadius)
    collisionMatrix = (collisionRadius >= totalDist)
    merges = []

    if (np.sum(collisionMatrix) > startPlanets):
        # obviously the diagonals are true
        for idx, a in np.ndenumerate(collisionMatrix):
            if((idx[0] != idx[1]) & a):
                merges = idx
                break
        if (merges != []):
            newMass = pData['mass'][merges[0]] + pData['mass'][merges[1]]
            newPos = (pData['position'][merges[0]] * pData['mass'][merges[0]] + pData['position'][merges[1]] * pData['mass'][merges[1]]) / newMass
            newVel = (pData['velocity'][merges[0]] * pData['mass'][merges[0]] + pData['velocity'][merges[1]] * pData['mass'][merges[1]]) / newMass
            pData['position'][merges[0]] = newPos
            pData['velocity'][merges[0]] = newVel
            pData['mass'][merges[0]] = newMass
            pData['radius'][merges[0]] = np.cbrt(newMass / density)
            newpData, xdist, ydist, totalDistSqrd, totalDist, startPlanets = modelPlanetMerges(np.delete(pData, merges[1], 0))
            toggle = True
    else:
        newpData = pData
    if (toggle): 
        ic(newpData)
    return [newpData, xdist, ydist, totalDistSqrd, totalDist, startPlanets]




def animate(i):
    planData, xdist, ydist, totalDistSqrd, totalDist, totalPlanets = modelPlanetMerges(planetData)

    if (totalPlanets == 1):
        ic(planData)

    # Force = GMm/rsqrd => Accn = GM/rsqrd
    totalAccn = planData['mass'] * bigG / totalDistSqrd
    xAccn = totalAccn * xdist / totalDist
    yAccn = totalAccn * ydist / totalDist
    xNetAccn = xAccn.sum(axis = 1)
    yNetAccn = yAccn.sum(axis = 1)

    # Update Positions and Velocities
    planData['position'][:, 0] += planData['velocity'][:,0] * dt
    planData['position'][:, 1] += planData['velocity'][:,1] * dt
    planData['velocity'][:, 0] += xNetAccn * dt
    planData['velocity'][:, 1] += yNetAccn * dt
    sc.set_offsets(planData['position'])
    sc.set_array(planData['mass'].flatten())
    sc.set_sizes(planData['radius'].flatten() * sizeMulti)
    return sc

ani = matplotlib.animation.FuncAnimation(fig, animate, frames = 2, interval = 100, repeat = True)
plt.show()