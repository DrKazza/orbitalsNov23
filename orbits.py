from matplotlib import pyplot as plt
import matplotlib.animation
import numpy as np

# Assign global variables, time interval and bigG#
bigG = 10000
dt = 0.01
density = 1

# Assign starting points
planetData = np.zeros(3, dtype= [('position', float, (2,)),
                                ('velocity', float, (2,)),
                                ('mass', float, (1,))])
planetData['position'] = np.array([[50, 75],
                       [-30, 15],
                       [0, -10]])
planetData['velocity'] = np.array([[-1, -2],
                       [1, -2],
                       [0, 0]])
planetData['mass'] = np.array([[1], [1], [2]])


fig, ax = plt.subplots()
plt.xlim(-100,100)
plt.ylim(-100,100)
sc = ax.scatter(x = planetData['position'][:, 0], y= planetData['position'][:, 1], c= planetData['mass'], s= planetData['mass']*100)


def modelPlanetMerges(pData):
    startPlanets = pData.ndim + 1 

    xdist = np.tile(planetData['position'][0], (startPlanets,1))
    xdist -= np.transpose(xdist)
    ydist = np.tile(planetData[:,1], (startPlanets,1))
    ydist -= np.transpose(ydist)
    totalDistSqrd = xdist * xdist + ydist * ydist
    # Make zero distances non-zero to avoid div0 errors
    totalDistSqrd += (totalDistSqrd == 0) * 1
    totalDist = np.sqrt(totalDistSqrd)

    return [newpData, xdist, ydist, totalPlanets]




def animate(i):
#    planetData, xdist, ydist, totalPlanets = modelPlanetMerges(planetData)
    totalPlanets = len(planetData)
    xdist = np.tile(planetData['position'][:,0], (totalPlanets,1))
    xdist -= np.transpose(xdist)
    ydist = np.tile(planetData['position'][:,1], (totalPlanets,1))
    ydist -= np.transpose(ydist)
    totalDistSqrd = xdist * xdist + ydist * ydist
    # Make zero distances non-zero to avoid div0 errors
    totalDistSqrd += (totalDistSqrd == 0) * 1
    totalDist = np.sqrt(totalDistSqrd)

    # Force = GMm/rsqrd => Accn = GM/rsqrd
    totalAccn = planetData['mass'] * bigG / totalDistSqrd
    xAccn = totalAccn * xdist / totalDist
    yAccn = totalAccn * ydist / totalDist
    xNetAccn = xAccn.sum(axis = 1)
    yNetAccn = yAccn.sum(axis = 1)

    # Update Positions and Velocities
    planetData['position'][:, 0] += planetData['velocity'][:,0] * dt
    planetData['position'][:, 1] += planetData['velocity'][:,1] * dt
    planetData['velocity'][:, 0] += xNetAccn * dt
    planetData['velocity'][:, 1] += yNetAccn * dt
    sc.set_offsets(planetData['position'])
    return sc

ani = matplotlib.animation.FuncAnimation(fig, animate, frames = 2, interval = 100, repeat = True)
plt.show()
