import numpy as np
from icecream import ic
import pygame
pygame.init()

# Assign global variables, time interval and bigG#
bigG = 10000
dt = 0.01
density = 0.1
speedScalar = 0.05
totalParticles = 1000

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

def drawParticles(partics):
    for part in partics:
        [xCoord, yCoord] = part['position']
        radius = part['radius']
        pygame.draw.circle(WIN, WHITE, (xCoord + WIDTH / 2, yCoord + HEIGHT / 2), radius[0])


def main():
    run = True
    clock = pygame.time.Clock()

    particles = generateParticles(totalParticles, speedScalar)

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update Positions and Velocities
        particles['position'][:, 0] += particles['velocity'][:,0] * dt
        particles['position'][:, 1] += particles['velocity'][:,1] * dt
        particles['velocity'][:, 0] += -particles['position'][:, 1] * speedScalar
        particles['velocity'][:, 1] += particles['position'][:, 0] * speedScalar

        drawParticles(particles)
        pygame.display.update()

    pygame.quit()


main()

