from classcurve import *
from algorithms import *

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
ip = 0  # indeks aktualnego punktu
n = 0  # liczba krzywych
activtext = "1"
activx = "0"
activy = "0"

actcurindlabel = Gtk.Label(i+1)
actpointindlabel = Gtk.Label(ip+1)


fig, ax = plt.subplots()
ax.set(xlim=(0, 100), ylim=(0, 100))
ax.plot([], [])
canvas = FigureCanvas(fig)  # a Gtk.DrawingArea

# obsluga myszki - podlaczenia
#canv_add_point = canvas.mpl_connect('button_press_event', add_point_to)
canv_add_point = None
canv_motion = None
canv_release = None
press = 0


def show_curves():
    global curves, i, ip
    plt.cla()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    nc = 0
    for c in curves:
        if c.visibility == 1:
            if c.type == 1:
                ax.plot(c.x, c.y, label=i, linewidth=c.thick, color=c.color)
            if c.type == 2:
                if c.i > 1:
                    t1 = np.arange(0.0, 100.0, 0.1)
                    ax.plot(t1, Lagrange(t1, c.x, c.y, c.i), label=i,
                            linewidth=c.thick, color=c.color)
            if c.type == 3:
                if c.i > 1:
                    # t1 = np.arange(0.0, 100.0, 0.1)
                    # ax.plot(Bezier(t1, 0, 100, c.x, c.i), Bezier(t1, 0, 100, c.y, c.i), label=i,
                    #       linewidth=c.thick, color=c.color)
                    t1 = np.arange(c.x[0], c.x[c.i-1], 0.1)
                    ax.plot(Bezier(t1, c.x[0], c.x[c.i-1], c.x, c.i), Bezier(t1, c.x[0], c.x[c.i-1], c.y, c.i), label=i,
                            linewidth=c.thick, color=c.color)
            if c.type == 4:
                if c.i > i:
                    # print("here")
                    M = deterMnifs3(c.x, c.y, c.i)
                    # print("here")
                    for k in range(1, c.i):
                        # print(k)
                        mx = max(c.x[k-1], c.x[k])
                        mn = min(c.x[k-1], c.x[k])
                        hk = mx-mn
                        t1 = np.arange(mn, mx, hk/100)
                        ax.plot(t1, NISF3(t1, c.x[k], c.y[k], c.x[k-1], c.y[k-1], M[k], M[k-1]), label=i,
                                linewidth=c.thick, color=c.color)
                        # ax.plot(t1, t1,
                        #       linewidth=c.thick, color=c.color)
            if c.type == 5:
                if c.i > i:
                    # print("here")
                    M = deterMnofs3(c.x, c.y, c.i)
                    # print("here")
                    for k in range(1, c.i):
                        # print(k)
                        mx = max(c.x[k-1], c.x[k])
                        mn = min(c.x[k-1], c.x[k])
                        hk = mx-mn
                        t1 = np.arange(mn, mx, hk/100)
                        ax.plot(t1, OISF3(t1, c.x[k], c.y[k], c.x[k-1], c.y[k-1], M[k], M[k-1]), label=i,
                                linewidth=c.thick, color=c.color)
                        # ax.plot(t1, t1,
                        #       linewidth=c.thick, color=c.color)
            if c.i > 1:
                ax.annotate(str(nc+1),
                            ((9*c.x[0]+c.x[1])/10, (9*c.y[0]+c.y[1])/10), color="red")
    for c in curves:
        if c.control_points:
            ax.plot(c.x, c.y, ".", color=c.color)
            if curves[i] == c:
                if c.color != 'red':
                    # print("here")
                    ax.plot(c.x[ip], c.y[ip], ".", color='red')
                else:
                    ax.plot(c.x[ip], c.y[ip], color='blue')
            for j in range(1, c.i+1):
                ax.annotate(j, (c.x[j-1], c.y[j-1]))
    canvas.draw_idle()


def add_point_to(event):
    global curves, i, n
    if n > 0:
        c = curves[i]
        c.add_point(event.xdata, event.ydata)
        curves[i] = c
        show_curves()


def change_point(event):
    global curves, n, i, ip
    cp = np.array((event.xdata, event.ydata))
    dist = 10000
    probpoint = ip
    probcurve = i
    for j in range(0, n):
        c = curves[j]
        for k in range(0, c.i):
            po = np.array((c.x[k], c.y[k]))
            curdist = np.linalg.norm(po-cp)
            if curdist < dist and curdist < 1:
                dist = curdist
                probpoint = k
                probcurve = j
    i = probcurve
    ip = probpoint
    actcurindlabel.set_text(str(i+1))
    actpointindlabel.set_text(str(ip+1))
    show_curves()


def moving_point(event):
    global press
    press = 1


def on_motion(event):
    global press, curves, i, ip
    if press == 1:
        c = curves[i]
        c.x[ip] = event.xdata
        c.y[ip] = event.ydata
        show_curves()


def on_release(event):
    global press
    press = 0
    show_curves()


def move_point(event):
    global canv_add_point, canvas
    canvas.mpl_disconnect(canv_add_point)
    #canv_choose_point = canvas.mpl_connect('button_press_event', change_point)
    canv_add_point = canvas.mpl_connect('button_press_event', moving_point)
    canv_motion = canvas.mpl_connect('motion_notify_event', on_motion)
    canv_release = canvas.mpl_connect('button_release_event', on_release)


def choose_point(event):
    global canv_add_point, canvas
    canvas.mpl_disconnect(canv_add_point)
    #canv_choose_point = canvas.mpl_connect('button_press_event', change_point)
    canv_add_point = canvas.mpl_connect('button_press_event', change_point)


def add_point(event):
    global canv_add_point
    canvas.mpl_disconnect(canv_add_point)
    #canv_choose_point = canvas.mpl_connect('button_press_event', change_point)
    canv_add_point = canvas.mpl_connect('button_press_event', add_point_to)


def new_curve(event):
    global curves, i, n, canvas, canv_add_point
    canvas.mpl_disconnect(canv_add_point)
    canv_add_point = canvas.mpl_connect('button_press_event', add_point_to)
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
    global curves, i, activtext, canvas
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
    actcurindlabel.set_text(str(i+1))


def del_point(event):
    global curves, activtext, i, ip
    c = curves[i]
    c.remove_point(ip)
    if ip > 0:
        ip = ip-1
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
    k = int(activx)-1
    l = int(activy)-1
    if k < c.i and l < c.i:
        c.swap_points(k, l)
    show_curves()


def undo(event):
    global curves, i, ip
    c = curves[i]
    if ip == c.i-1:
        ip = 0
    c.remove_point(c.i-1)
    show_curves()


def change_type(event):
    global curves, i, activtext
    c = curves[i]
    c.change_type(int(activtext))
    show_curves()


def division_curve_point(event):
    global curves, i, n, activtext
    # print("here")
    c = curves[i]
    if c.type == 3:
        t = int(activtext)
        # if t>=c.x[0] and t<=c.x[n-1]:
        X = c.x
        Y = c.y
        np = c.i
        c.x, c.y = deCasteljauleft(t, X[0], X[np-1], X, Y, np)
        # print(c.x)
        d = Curve()
        d.i = c.i
        d.type = c.type
        d.color = c.color
        d.thick = c.thick
        d.x, d.y = deCasteljauright(t, X[0], X[np-1], X, Y, np)
        n += 1
        curves.append(d)
        show_curves()
