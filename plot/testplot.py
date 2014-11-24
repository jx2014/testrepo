import numpy as np
import matplotlib.pyplot as plt

Y, X = np.mgrid[-30:30:100j, -30:30:100j]
U = X*X
V = Y*Y*Y
speed = np.sqrt(U*U + V*V)


plt.streamplot(X, Y, U, V, color=U, linewidth=1, cmap=plt.cm.autumn, density=[1, 1])
plt.colorbar()
# 
f, (ax1, ax2) = plt.subplots(ncols=2)
ax1.streamplot(X, Y, U, V, density=[0.5, 1])
# 
lw = 5*speed/speed.max()
ax2.streamplot(X, Y, U, V, density=0.6, color='k', linewidth=lw)

plt.show()