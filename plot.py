from classcurve import *
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np


curves = []
i = 0  # indeks aktualnej krzywej
n = 0  # liczba krzywych

fig, ax = plt.subplots()
ax.set(xlim=(0, 100), ylim=(0, 100))
ax.plot([], [])

# poprawić wyświetlanie wszystkich dotychczasowych kryzwych no i kolorki ogarnąć


def add_point_to(event):
    global curves, i
    c = curves[i]
    c.add_point(event.xdata, event.ydata)
    curves[i] = c
    show_curves()


def show_curves():
    global curves
    for c in curves:
        ax.plot(c.x, c.y, color=c.color)
    for c in curves:
        if c.control_points:
            ax.plot(c.x, c.y, ".", color=c.color)
    plt.show()


def new_curve():
    global curves, i, n
    c = Curve()
    curves.append(c)
    i = n
    n += 1


new_curve()
cid = fig.canvas.mpl_connect('button_press_event', add_point_to)
plt.show()
