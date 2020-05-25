from classcurve import *
from menu_functions import *
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import numpy as np
from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.set_default_size(1000, 800)
win.set_title("(Jeszcze nie) najlepszy na świecie edytor krzywych")

grid = Gtk.Grid()
grid.set_column_spacing(10)
win.add(grid)


genlabel = Gtk.Label("Funkcje ogólne")
grid.attach(genlabel, 0, 0, 1, 1)
btnnew = Gtk.Button(label="Nowa krzywa")
grid.attach(btnnew, 0, 1, 1, 1)
btnnew.connect("clicked", new_curve)
btnchange = Gtk.Button(label="Zmień krzywą")
grid.attach(btnchange, 0, 2, 1, 1)
btnchange.connect("clicked", change_activ_curve)

curlabel = Gtk.Label("Obsługa krzywej")
grid.attach(curlabel, 0, 4, 1, 1)
btnchangetype = Gtk.Button(label="Zmień typ krzywej")
grid.attach(btnchangetype, 0, 5, 1, 1)
btnchangetype.connect("clicked", change_type)
btnshift = Gtk.Button(label="Przesuń krzywą")
grid.attach(btnshift, 0, 6, 1, 1)
btnshift.connect("clicked", shift_curve)
btndivcur = Gtk.Button(label="Podziel krzywą")
grid.attach(btndivcur, 0, 7, 1, 1)
btndivcur.connect("clicked", division_curve_point)

looklabel = Gtk.Label("Wygląd krzywej")
grid.attach(looklabel, 0, 8, 1, 1)
btncolor = Gtk.Button(label="Zmień kolor")
grid.attach(btncolor, 0, 9, 1, 1)
btncolor.connect("clicked", change_color_of)
btncolor = Gtk.Button(label="Zmień grubość")
grid.attach(btncolor, 0, 10, 1, 1)
btncolor.connect("clicked", change_thick_of)
btnshow = Gtk.Button(label="Pokaż / ukryj krzywą")
grid.attach(btnshow, 0, 11, 1, 1)
btnshow.connect("clicked", show_cover_curve)

pointlabel = Gtk.Label("Obsługa punktów")
grid.attach(pointlabel, 0, 12, 1, 1)
btnshowpoints = Gtk.Button(label="Pokaż / ukryj punkty kontrolne")
grid.attach(btnshowpoints, 0, 13, 1, 1)
btnshowpoints.connect("clicked", show_cover_points)
btndelp = Gtk.Button(label="Usuń punkt")
grid.attach(btndelp, 0, 14, 1, 1)
btndelp.connect("clicked", del_point)
btnswap = Gtk.Button(label="Zamień punkty")
grid.attach(btnswap, 0, 15, 1, 1)
btnswap.connect("clicked", swap_p)
btnchangepoint = Gtk.Button(label="Wybierz punkt")
grid.attach(btnchangepoint, 0, 16, 1, 1)
btnchangepoint.connect("clicked", choose_point)
btnaddpoint = Gtk.Button(label="Dodaj punkt")
grid.attach(btnaddpoint, 0, 17, 1, 1)
btnaddpoint.connect("clicked", add_point)
btnmovepoint = Gtk.Button(label="Przesuń punkt")
grid.attach(btnmovepoint, 0, 18, 1, 1)
btnmovepoint.connect("clicked", move_point)


btnundo = Gtk.Button(label="Cofnij dodanie punktu")
grid.attach(btnundo, 10, 0, 1, 1)
btnundo.connect("clicked", undo)


entry = Gtk.Entry()
grid.attach(entry, 1, 0, 1, 1)
entry.connect("key-release-event", change_activtext)
entryx = Gtk.Entry()
grid.attach(entryx, 7, 0, 1, 1)
entryx.connect("key-release-event", change_activx)
entryy = Gtk.Entry()
grid.attach(entryy, 9, 0, 1, 1)
entryy.connect("key-release-event", change_activy)


activcurvelabel = Gtk.Label("Krzywa:")
grid.attach(activcurvelabel, 2, 0, 1, 1)
grid.attach(actcurindlabel, 3, 0, 1, 1)
activpointlabel = Gtk.Label("Punkt:")
grid.attach(activpointlabel, 4, 0, 1, 1)
grid.attach(actpointindlabel, 5, 0, 1, 1)
xlabel = Gtk.Label("x")
grid.attach(xlabel, 6, 0, 1, 1)
ylabel = Gtk.Label("y")
grid.attach(ylabel, 8, 0, 1, 1)

sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
# win.add(sw)
grid.attach(sw, 1, 1, 40, 40)


#canvas.mpl_connect('button_press_event', add_point_to)

canvas.set_size_request(800, 600)
sw.add_with_viewport(canvas)
canvas.draw_idle()
win.show_all()
Gtk.main()
