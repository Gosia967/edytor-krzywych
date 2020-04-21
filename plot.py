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
activtext = ""

fig, ax = plt.subplots()
ax.set(xlim=(0, 100), ylim=(0, 100))
ax.plot([], [])

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.set_default_size(1000, 800)
win.set_title("Embedding in GTK")

#entry = Gtk.Entry()
#entry.set_text("Hello World")
#vbox.pack_start(win.entry, True, True, 0)
# win.add(entry)


def add_point_to(event):
    global curves, i, n
    if n > 0:
        c = curves[i]
        c.add_point(event.xdata, event.ydata)
        curves[i] = c
        show_curves()


def show_curves():
    global curves
    for c in curves:
        ax.plot(c.x, c.y, label=i, linewidth=c.thick, color=c.color)
    for c in curves:
        if c.control_points:
            ax.plot(c.x, c.y, ".", color=c.color)
    canvas.draw_idle()


def new_curve(event):
    global curves, i, n
    c = Curve()
    curves.append(c)
    i = n
    n += 1


def change_activtext(widget, event):
    global activtext
    activtext = widget.get_text()


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

# new_curve()
#cid = fig.canvas.mpl_connect('button_press_event', add_point_to)
# plt.show()


# A scrolled window border goes outside the scrollbars and viewport
# sw.set_border_width(10)

grid = Gtk.Grid()
grid.set_column_spacing(5)
win.add(grid)

btnnew = Gtk.Button(label="Nowa krzywa")
grid.attach(btnnew, 0, 0, 1, 1)
btnnew.connect("clicked", new_curve)
btncolor = Gtk.Button(label="Zmień kolor")
grid.attach(btncolor, 0, 1, 1, 1)
btncolor.connect("clicked", change_color_of)
btncolor = Gtk.Button(label="Zmień grubość")
grid.attach(btncolor, 0, 2, 1, 1)
btncolor.connect("clicked", change_thick_of)

entry = Gtk.Entry()
grid.attach(entry, 1, 0, 1, 1)
entry.connect("key-release-event", change_activtext)

sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
# win.add(sw)
grid.attach(sw, 1, 1, 40, 40)
canvas = FigureCanvas(fig)  # a Gtk.DrawingArea

canvas.mpl_connect('button_press_event', add_point_to)

canvas.set_size_request(800, 600)
sw.add_with_viewport(canvas)
canvas.draw_idle()
win.show_all()
Gtk.main()
