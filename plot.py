import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np


xs = np.array([])
ys = np.array([])
x = np.array([])
y = np.array([])
xs = np.append(xs, [x])
ys = np.append(ys, [y])
i = 0  # indeks aktualnej krzywej
n = 0  # liczba krzywych

fig, ax = plt.subplots()
ax.set(xlim=(0, 100), ylim=(0, 100))
ax.plot(x, y)

# poprawić wyświetlanie wszystkich dotychczasowych kryzwych no i kolorki ogarnąć


def add_point(event):
    global x, xs, i
    global y, ys
    x = np.append(x, [event.xdata])
    y = np.append(y, [event.ydata])
    xs[i] = x
    ys[i] = y
    ax.plot(x, y, ".")
    ax.plot(x, y)
    plt.show()


def shiftv(vx, vy):
    global x, y, xs, ys, i
    x = x+vx
    y = y+vy


def new_curve():
    global xs, ys, x, y, i, n
    x = np.array([])
    y = np.array([])
    xs = np.append(xs, [x])
    ys = np.append(ys, [y])
    i = n
    n += 1


cid = fig.canvas.mpl_connect('button_press_event', add_point)
plt.show()

print(x[99])
