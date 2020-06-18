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
btntrans = Gtk.Button(label="Transponuj")
grid.attach(btntrans, 0, 3, 1, 1)
btntrans.connect("clicked", transpose)
btnG1 = Gtk.Button(label="Połącz (G1)")
grid.attach(btnG1, 0, 4, 1, 1)
btnG1.connect("clicked", G1)
btnC1 = Gtk.Button(label="Połącz (C1)")
grid.attach(btnC1, 0, 5, 1, 1)
btnC1.connect("clicked", C1)
btnjoin = Gtk.Button(label="Scal krzywe")
grid.attach(btnjoin, 0, 6, 1, 1)
btnjoin.connect("clicked", join)


curlabel = Gtk.Label("Obsługa krzywej")
grid.attach(curlabel, 0, 7, 1, 1)
btnchangetype = Gtk.Button(label="Zmień typ krzywej")
grid.attach(btnchangetype, 0, 11, 1, 1)
btnchangetype.connect("clicked", change_type)
btnshift = Gtk.Button(label="Przesuń krzywą")
grid.attach(btnshift, 0, 14, 1, 1)
btnshift.connect("clicked", shift_curve)
btndivcur = Gtk.Button(label="Podziel krzywą (B)")
grid.attach(btndivcur, 0, 15, 1, 1)
btndivcur.connect("clicked", division_curve_point)
btndelcur = Gtk.Button(label="Usuń krzywą")
grid.attach(btndelcur, 0, 8, 1, 1)
btndelcur.connect("clicked", del_curve)
btndegup = Gtk.Button(label="Podnieś stopień (B)")
grid.attach(btndegup, 0, 9, 1, 1)
btndegup.connect("clicked", updeg)
btndegdown = Gtk.Button(label="Obniż stopień (B)")
grid.attach(btndegdown, 0, 10, 1, 1)
btndegdown.connect("clicked", downdeg)
btnscale = Gtk.Button(label="Skaluj")
grid.attach(btnscale, 0, 13, 1, 1)
btnscale.connect("clicked", scale)
btnrotate = Gtk.Button(label="Obróć")
grid.attach(btnrotate, 0, 12, 1, 1)
btnrotate.connect("clicked", rotate)

looklabel = Gtk.Label("Wygląd krzywej")
grid.attach(looklabel, 0, 16, 1, 1)
btncolor = Gtk.Button(label="Zmień kolor")
grid.attach(btncolor, 0, 19, 1, 1)
btncolor.connect("clicked", change_color_of)
btncolor = Gtk.Button(label="Zmień grubość")
grid.attach(btncolor, 0, 17, 1, 1)
btncolor.connect("clicked", change_thick_of)
btnshow = Gtk.Button(label="Pokaż / ukryj krzywą")
grid.attach(btnshow, 0, 18, 1, 1)
btnshow.connect("clicked", show_cover_curve)

pointlabel = Gtk.Label("Obsługa punktów")
grid.attach(pointlabel, 0, 20, 1, 1)
btnshowpoints = Gtk.Button(label="Pokaż / ukryj punkty kontrolne")
grid.attach(btnshowpoints, 0, 31, 1, 1)
btnshowpoints.connect("clicked", show_cover_points)
btndelp = Gtk.Button(label="Usuń punkt")
grid.attach(btndelp, 0, 21, 1, 1)
btndelp.connect("clicked", del_point)
btnswap = Gtk.Button(label="Zamień punkty")
grid.attach(btnswap, 0, 22, 1, 1)
btnswap.connect("clicked", swap_p)
btnchangepoint = Gtk.Button(label="Wybierz punkt")
grid.attach(btnchangepoint, 0, 23, 1, 1)
btnchangepoint.connect("clicked", choose_point)
btnaddpoint = Gtk.Button(label="Dodaj punkt")
grid.attach(btnaddpoint, 0, 24, 1, 1)
btnaddpoint.connect("clicked", add_point)
btnmovepoint = Gtk.Button(label="Przesuń punkt")
grid.attach(btnmovepoint, 0, 25, 1, 1)
btnmovepoint.connect("clicked", move_point)
btnweight = Gtk.Button(label="Zmień wagę")
grid.attach(btnweight, 0, 29, 1, 1)
btnweight.connect("clicked", change_weight)
btncolorcp = Gtk.Button(label="Zmień kolor punktów kontrolnych")
grid.attach(btncolorcp, 0, 26, 1, 1)
btncolorcp.connect("clicked", change_points_color)
btnsizecp = Gtk.Button(label="Zmień rozmiar punktów kontrolnych")
grid.attach(btnsizecp, 0, 27, 1, 1)
btnsizecp.connect("clicked", change_points_size)
btnrev = Gtk.Button(label="Odwróć kolejność punktów")
grid.attach(btnrev, 0, 28, 1, 1)
btnrev.connect("clicked", reverse_points)
btnval = Gtk.Button(label="Wartosć punktu")
grid.attach(btnval, 0, 30, 1, 1)
btnval.connect("clicked", point_value)


btnundo = Gtk.Button(label="Cofnij dodanie punktu")
grid.attach(btnundo, 10, 0, 1, 1)
btnundo.connect("clicked", undo)
btnsave = Gtk.Button(label="Zapisz obrazek")
grid.attach(btnsave, 11, 0, 1, 1)
btnsave.connect("clicked", save)
btninfo = Gtk.Button(label="Info")
grid.attach(btninfo, 12, 0, 1, 1)
btninfo.connect("clicked", show_dialog)


entry = Gtk.Entry()
grid.attach(entry, 1, 0, 1, 1)
entry.connect("key-release-event", change_activtext)
grid.attach(entryx, 7, 0, 1, 1)
entryx.connect("key-release-event", change_activx)
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
grid.attach(sw, 1, 1, 60, 100)  # 40,40


#canvas.mpl_connect('button_press_event', add_point_to)

canvas.set_size_request(600, 600)  # 800, 600
sw.add_with_viewport(canvas)
canvas.draw_idle()
win.show_all()
Gtk.main()
