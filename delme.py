import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

fig, ax = plt.subplots()
x, y = [], []
sc = ax.scatter(x,y)
plt.xlim(0,10)
plt.ylim(0,10)

def animate(i):
    x.append(np.random.rand(1)*10)
    y.append(np.random.rand(1)*10)#
    sc.set_offsets(np.c_[x,y])

#ani = matplotlib.animation.FuncAnimation(fig, animate, frames = 2, interval = 100, repeat = True)
#plt.show()

n = 5
particles = np.zeros(n, dtype= [("position", float, 2),
                                ("velocity", float, 2),
                                ("force", float, 2),
                                ("size", float, 1)])

particles["position"]=np.random.uniform(0,1,(n,2))
particles["size"]=0.5 * np.ones(n)

print(len(particles))
