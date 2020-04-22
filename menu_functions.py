from classcurve import *

import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import numpy as np
from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')

curves = []
i = 0  # indeks aktualnej krzywej
n = 0  # liczba krzywych
activtext = "1"
activx = "0"
activy = "0"

actcurindlabel = Gtk.Label(i)

fig, ax = plt.subplots()
ax.set(xlim=(0, 100), ylim=(0, 100))
ax.plot([], [])
canvas = FigureCanvas(fig)  # a Gtk.DrawingArea


def show_curves():
    global curves, i
    plt.cla()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    for c in curves:
        if c.visibility == 1:
            ax.plot(c.x, c.y, label=i, linewidth=c.thick, color=c.color)
            ax.legend()
            # plt.gca().add_artist(plt.legend())
    for c in curves:
        if c.control_points:
            ax.plot(c.x, c.y, ".", color=c.color)
    canvas.draw_idle()


def add_point_to(event):
    global curves, i, n
    if n > 0:
        c = curves[i]
        c.add_point(event.xdata, event.ydata)
        curves[i] = c
        show_curves()


def new_curve(event):
    global curves, i, n
    c = Curve()
    curves.append(c)
    i = n
    n += 1
    actcurindlabel.set_text(str(i))


def change_activtext(widget, event):
    global activtext
    activtext = widget.get_text()


def change_activx(widget, event):
    global activx
    activx = widget.get_text()


def change_activy(widget, event):
    global activy
    activy = widget.get_text()


def change_color_of(event):
    global curves, i, activtext
    c = curves[i]
    c.change_color(activtext)
    show_curves()


def change_thick_of(event):
    global curves, i, activtext
    c = curves[i]
    c.change_thick(activtext)
    show_curves()


def show_cover_curve(event):
    global curves, i
    c = curves[i]
    if c.visibility == 1:
        c.cover_curve()
    else:
        c.show_curve()
    show_curves()


def show_cover_points(event):
    global curves, i
    c = curves[i]
    if c.control_points == 1:
        c.cover_control_points()
    else:
        c.show_control_points()
    show_curves()


def change_activ_curve(event):
    global i, activtext, n
    k = int(activtext)
    if k < n:
        i = k
    actcurindlabel.set_text(str(i))


def del_point(event):
    global curves, activtext, i
    c = curves[i]
    pind = int(activtext)
    if pind < c.i:
        c.remove_point(pind)
    show_curves()


def shift_curve(event):
    global curves, activx, activy, i
    c = curves[i]
    x = int(activx)
    y = int(activy)
    c.shiftv(x, y)
    show_curves()


def swap_p(event):
    global curves, activx, activy, i
    c = curves[i]
    k = int(activx)
    l = int(activy)
    if k < c.i and l < c.i:
        c.swap_points(k, l)
    show_curves()


def undo(event):
    global curves, i
    c = curves[i]
    c.remove_point(c.i-1)
    show_curves()
