import numpy as np
from icecream import ic
import pygame
pygame.init()

# Assign global variables, time interval and bigG#
bigG = 1000
dt = 0.01
density = 0.1
totalParticles = 200
initialRotation = 0.2

# Set up Pygame variables
WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation")

# Set up colours
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (188,39,50)
GREEN = (0,255,0)
BLUE = (100,149,237)
DARK_GREY = (80,78,81)


def generateParticles(numParts, rotationSpeed):
    # Assign starting points
    particleData = np.zeros(numParts, dtype= [('position', float, (2,)),
                                    ('velocity', float, (2,)),
                                    ('mass', float, (1,)),
                                    ('radius', float, (1,))])
    particleData['position'] = (np.random.rand(numParts, 2) - 0.5) * [WIDTH / 2, HEIGHT / 2]
    particleData['mass'] = np.ones((numParts, 1))

    # Calculated starting points
    particleData['radius'] = np.cbrt(particleData['mass'] / density)
    particleData['velocity'][:,0] = -particleData['position'][:,1]
    particleData['velocity'][:,1] = particleData['position'][:,0]
    particleData['velocity'] *= rotationSpeed
    return particleData


def defineParticles():
    # Assign starting points
    particleData = np.zeros(3, dtype= [('position', float, (2,)),
                                    ('velocity', float, (2,)),
                                    ('mass', float, (1,)),
                                    ('radius', float, (1,))])
    particleData['position'] = np.array([[50, 75],
                        [-30, 15],
                        [0, -10]])
    particleData['velocity'] = np.array([[-1, -2],
                        [1, -2],
                        [0, 0]])
    particleData['mass'] = np.array([[1], [2], [3]])

    # Calculated starting points
    particleData['radius'] = np.cbrt(particleData['mass'] / density)
    return particleData


def drawParticles(partics):
    for part in partics:
        [xCoord, yCoord] = part['position']
        radius = part['radius']
        pygame.draw.circle(WIN, WHITE, (xCoord + WIDTH / 2, yCoord + HEIGHT / 2), radius[0])

def calcParticlePos(partics):
    numPartics = len(partics)
    smallestRadius = np.min(partics['radius'])
    xdist = np.tile(partics['position'][:, 0], (numPartics,1))
    xdist -= np.transpose(xdist)
    ydist = np.tile(partics['position'][:, 1], (numPartics,1))
    ydist -= np.transpose(ydist)
    totalDistSqrd = xdist * xdist + ydist * ydist
    # Make zero distances non-zero to avoid div0 errors
    totalDistSqrd += (totalDistSqrd == 0) * smallestRadius
    totalDist = np.sqrt(totalDistSqrd)
    collisionRadius = np.tile(partics['radius'], numPartics)
    collisionRadius += np.transpose(collisionRadius)
    collisionMatrix = (collisionRadius >= totalDist)

    if (np.sum(collisionMatrix) > numPartics):
        i1, i2 = np.where(collisionMatrix == True)
        for a,b in zip(i1, i2):
            if a != b:
                merges= (b,a)
                # why do we swap them round? because we're taking the final value
                # in the matrix match then a will always be bigger than b and also collisionMatrix is symmetric
        newMass = partics['mass'][merges[0]] + partics['mass'][merges[1]]
        newPos = (partics['position'][merges[0]] * partics['mass'][merges[0]] + partics['position'][merges[1]] * partics['mass'][merges[1]]) / newMass
        newVel = (partics['velocity'][merges[0]] * partics['mass'][merges[0]] + partics['velocity'][merges[1]] * partics['mass'][merges[1]]) / newMass
        partics['position'][merges[0]] = newPos
        partics['velocity'][merges[0]] = newVel
        partics['mass'][merges[0]] = newMass
        partics['radius'][merges[0]] = np.cbrt(newMass / density)
        oneLessPartic = np.delete(partics, merges[1], 0)
        # here comes the recursion
        [newPdata, xdist, ydist, totalDistSqrd, totalDist, numPartics] = calcParticlePos(oneLessPartic)
    else:
        # there's been no collisions just return all the data nicely
        newPdata = partics

    return ([newPdata, xdist, ydist, totalDistSqrd, totalDist, numPartics])



def main():
    run = True
    clock = pygame.time.Clock()

    particles = generateParticles(totalParticles, initialRotation)

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        [particles, xdist, ydist, totalDistSqrd, totalDist, numParticles] = calcParticlePos(particles)

        # Force = GMm/rsqrd => Accn = GM/rsqrd
        totalAccn = particles['mass'] * bigG / totalDistSqrd
        xAccn = totalAccn * xdist / totalDist
        yAccn = totalAccn * ydist / totalDist
        xNetAccn = xAccn.sum(axis = 1)
        yNetAccn = yAccn.sum(axis = 1)

        # Update Positions and Velocities
        particles['position'][:, 0] += particles['velocity'][:,0] * dt
        particles['position'][:, 1] += particles['velocity'][:,1] * dt
        particles['velocity'][:, 0] += xNetAccn * dt
        particles['velocity'][:, 1] += yNetAccn * dt

        drawParticles(particles)
        pygame.display.update()

    pygame.quit()


main()

