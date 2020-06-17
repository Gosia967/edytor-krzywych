from time import sleep
from classcurve import *
from algorithms import *

import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib import colors as mcolors
import numpy as np
from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')

curves = []
i = 0  # indeks aktualnej krzywej
ip = 0  # indeks aktualnego punktu
n = 0  # liczba krzywych
entryx = Gtk.Entry()
entryy = Gtk.Entry()
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
# canv_add_point = canvas.mpl_connect('button_press_event', add_point_to)
canv_add_point = None
canv_motion = None
canv_release = None
press = 0


def show_curves():
    global curves, i, ip
    plt.cla()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    nclabel = 0
    for c in curves:
        if c.visibility == 1:
            if c.type == 1:
                # print("nie śpię")
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
                    mn = min(c.x[0], c.x[c.i-1])
                    mx = max(c.x[0], c.x[c.i-1])
                    t1 = np.arange(mn, mx, 0.01)
                    ax.plot(Bezier(t1, c.x[0], c.x[c.i-1], c.x, c.i), Bezier(t1, c.x[0], c.x[c.i-1], c.y, c.i), label=i,
                            linewidth=c.thick, color=c.color)
                    # t1 = np.arange(c.x[0], c.x[c.i-1], 0.1)
                    # ax.plot(Bezier(t1, c.x[0], c.x[c.i-1], c.x, c.i), Bezier(t1, c.x[0], c.x[c.i-1], c.y, c.i), label=i,
                    #       linewidth=c.thick, color=c.color)
            if c.type == 6:
                if c.i > 1:
                    mn = min(c.x[0], c.x[c.i-1])
                    mx = max(c.x[0], c.x[c.i-1])
                    t1 = np.arange(mn, mx, 0.1)
                    ax.plot(ratBezier(t1, c.x[0], c.x[c.i-1], c.x, c.w, c.i), ratBezier(t1, c.x[0], c.x[c.i-1], c.y, c.w, c.i), label=i,
                            linewidth=c.thick, color=c.color)
            if c.type == 4:
                if c.i > 1:
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
                if c.i > 1:
                    M = deterMnofs3(c.x, c.y, c.i)
                    for k in range(1, c.i):
                        mx = max(c.x[k-1], c.x[k])
                        mn = min(c.x[k-1], c.x[k])
                        hk = mx-mn
                        t1 = np.arange(mn, mx, hk/100)
                        ax.plot(t1, OISF3(t1, c.x[k], c.y[k], c.x[k-1], c.y[k-1], M[k], M[k-1]), label=i,
                                linewidth=c.thick, color=c.color)
            if c.i > 1:
                ax.annotate(str(nclabel+1),
                            ((9*c.x[0]+c.x[1])/10, (9*c.y[0]+c.y[1])/10), color="red")
                nclabel += 1
            else:
                nclabel += 1

    for c in curves:
        if c.control_points and c.i > 0:
            ax.plot(c.x, c.y, ".", markersize=c.points_size,
                    color=c.points_color)
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
    global canv_add_point, canv_motion, canv_release, canvas
    canvas.mpl_disconnect(canv_add_point)
    # canv_choose_point = canvas.mpl_connect('button_press_event', change_point)
    canv_add_point = canvas.mpl_connect('button_press_event', moving_point)
    canv_motion = canvas.mpl_connect('motion_notify_event', on_motion)
    canv_release = canvas.mpl_connect('button_release_event', on_release)


def choose_point(event):
    global canv_add_point, canvas
    canvas.mpl_disconnect(canv_add_point)
    # canv_choose_point = canvas.mpl_connect('button_press_event', change_point)
    canv_add_point = canvas.mpl_connect('button_press_event', change_point)


def add_point(event):
    global canv_add_point
    canvas.mpl_disconnect(canv_add_point)
    # canv_choose_point = canvas.mpl_connect('button_press_event', change_point)
    canv_add_point = canvas.mpl_connect('button_press_event', add_point_to)


def new_curve(event):
    global curves, i, n, canvas, canv_add_point
    canvas.mpl_disconnect(canv_add_point)
    canv_add_point = canvas.mpl_connect('button_press_event', add_point_to)
    c = Curve()
    # curves.append(c)
    curves = np.append(curves, [c])
    i = n
    n += 1
    actcurindlabel.set_text(str(i+1))


def change_activtext(widget, event):
    global activtext
    activtext = widget.get_text()


def change_activx(widget, event):
    global activx
    activx = widget.get_text()


def change_activy(widget, event):
    global activy
    activy = widget.get_text()


def is_color(col):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                    for name, color in colors.items())
    sorted_names = [name for hsv, name in by_hsv]
    for i, name in enumerate(sorted_names):
        # print(name)
        if name == col:
            return True
    return False


def change_color_of(event):
    global curves, i, activtext, canvas
    c = curves[i]
    if (is_color(activtext)):
        c.change_color(activtext)
    show_curves()


def change_points_color(event):
    global curves, i, activtext
    c = curves[i]
    if (is_color(activtext)):
        c.change_point_color(activtext)
    show_curves()


def change_points_size(event):
    global curves, i, activtext
    c = curves[i]
    c.change_point_size(float(activtext))
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
    k = int(activtext) - 1
    if k < n:
        i = k
    actcurindlabel.set_text(str(i+1))
    show_curves()


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
    if c.i > 0:
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
        npp = c.i
        c.x, c.y = deCasteljauleft(t, X[0], X[npp-1], X, Y, npp)
        # print(c.x)
        d = Curve()
        d.i = c.i
        d.w = c.w
        d.type = c.type
        d.color = c.color
        d.thick = c.thick
        d.x, d.y = deCasteljauright(t, X[0], X[npp-1], X, Y, npp)
        n += 1
        curves = np.append(curves, [d])
        # print(curves)
        # curves.append(d)
        show_curves()


def change_weight(event):
    global curves, i, activtext, ip
    c = curves[i]
    c.change_weight(ip, int(activtext))
    show_curves()


def del_curve(event):
    global curves, i, n, ip
    if n > 0:
        if n == 1:
            curves = []
        elif n == 2:
            curves = np.delete(curves, i)
            # print("hello")
            # print(curves[0])
            c = curves[0]
            curves = []
            curves = np.append(curves, [c])
        else:
            curves = np.delete(curves, i)
        n -= 1
        ip = 0
        i = 0
        show_curves()


def transpose(event):
    # transpozycja a(activx) w b(activy)
    global curves, i, n, activx, activy
    a = int(activx) - 1
    b = int(activy)-1
    xp = curves[a].x
    yp = curves[a].y
    wp = curves[a].w
    alpha = 0.0
    delta = 0.1
    for k in range(0, 11):
        curves[a].x = alpha*curves[b].x + (1-alpha)*xp
        curves[a].y = alpha*curves[b].y + (1-alpha)*yp
        curves[a].w = alpha*curves[b].w + (1-alpha)*wp
        alpha += delta
        sleep(0.1)
        # print("śpij kochany śpij")
        show_curves()
    # curves[a].x = alpha*curves[b].x + (1-alpha)*xp
    # curves[a].y = alpha*curves[b].y + (1-alpha)*yp
    # curves[a].w = alpha*curves[b].w + (1-alpha)*wp
    # alpha += delta
    # sleep(0.1)
    #    print("śpij kochany śpij")
    # show_curves()


def downdeg(event):
    global curves, i, n
    c = curves[i]
    if c.type == 3:
        if c.i > 1:
            c.x, c.y = degdown(c.x, c.y, c.i)
            c.i -= 1
            c.w = np.delete(c.w, c.i)
            show_curves()


def updeg(event):
    global curves, i, n
    c = curves[i]
    if c.type == 3:
        c.x, c.y = degup(c.x, c.y, c.i)
        c.i += 1
        c.w = np.append(c.w, [1.0])
        show_curves()


def G1(event):
    global curves, i, activtext, n
    j = int(activtext) - 1
    if j < n:
       # print(i)
        # print(j)
        c = curves[i]
        d = curves[j]
        vx = c.x[c.i-1] - d.x[0]
        vy = c.y[c.i-1] - d.y[0]
        d.shiftv(vx, vy)
        pc = d.x[0]
        pa = c.x[0]
        pb = d.x[d.i-1]
        n1 = c.i-1
        m1 = d.i-1
        if d.i > 1:
            d.x[1] = (d.x[0]*(n1/(pc-pa)+m1/(pb-pc)) -
                      c.x[n1-1]*n1/(pc-pa))*(pb-pc)/m1
            d.y[1] = (d.y[0]*(n1/(pc-pa)+m1/(pb-pc)) -
                      c.y[n1-1]*n1/(pc-pa))*(pb-pc)/m1
        show_curves()


def C1(event):
    global curves, i, activtext, n
    j = int(activtext) - 1
    if j < n:
       # print(i)
        # print(j)
        c = curves[i]
        d = curves[j]
        vx = c.x[c.i-1] - d.x[0]
        vy = c.y[c.i-1] - d.y[0]
        d.shiftv(vx, vy)
        n1 = c.i-1
        m1 = d.i-1
        if d.i > 1:
            # d.x[1] = n1/(pc-pa)*(c.x[n1] - c.x[n1-1])*(pb-pc)/m1 + d.x[0]
            # d.y[1] = n1/(pc-pa)*(c.y[n1] - c.y[n1-1])*(pb-pc)/m1 + d.y[0]
            d.x[1] = d.x[0]*2 - c.x[n1-1]
            d.y[1] = d.y[0]*2 - c.y[n1-1]
        show_curves()


def scale(event):
    global curves, i, activtext
    c = curves[i]
    c.scale(float(activtext))
    show_curves()


def rotate(event):
    global curves, i, activtext
    c = curves[i]
    c.rotate(float(activtext))
    show_curves()


def save(event):
    global activtext
    plt.savefig(activtext)


def reverse_points(event):
    global curves, i
    c = curves[i]
    c.reverse_points()
    show_curves()


def show_dialog(event):
    dialog = Gtk.Dialog("Typy krzywych")
    lab1 = Gtk.Label("1 -- łamana")
    lab2 = Gtk.Label("2 -- krzywa interpolacyjna")
    lab3 = Gtk.Label("3 -- krzywa Beziera")
    lab4 = Gtk.Label("4 -- NIFS3")
    lab5 = Gtk.Label("5 -- OIFS3")
    lab6 = Gtk.Label("6 -- wymierna krzywa Beziera")
    buturl = Gtk.LinkButton(
        "https://matplotlib.org/examples/color/named_colors.html", "dostępne kolory")
    box = dialog.get_content_area()
    box.add(lab1)
    box.add(lab2)
    box.add(lab3)
    box.add(lab4)
    box.add(lab5)
    box.add(lab6)
    box.add(buturl)
    dialog.show_all()
    dialog.run()
    dialog.destroy()


def point_value(event):
    global curves, i, activtext, activx, activy, entryx, entryy
    vp = float(activtext)
    print(vp)
    c = curves[i]
    if c.type == 3:
        activx, activy = Bezierpointvalue(
            vp, c.x[0], c.x[c.i-1], c.x, c.y, c.i)
        # activx, activy = deCasteljau(vp, c.x[0], c.x[c.i-1], c.x, c.y, c.i)
        entryx.set_text(str(activx))
        entryy.set_text(str(activy))
