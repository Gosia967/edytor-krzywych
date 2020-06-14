import numpy as np
import math

# types:
# 1. polyline
# 2. Lagrange polynomial


class Curve:
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])
        self.w = np.array([])
        self.color = 'blue'
        self.thick = 1
        self.control_points = 1
        self.visibility = 1
        self.type = 1
        self.i = 0  # liczba punktow
        self.points_color = 'blue'

    def add_point(self, ax, ay):
        self.x = np.append(self.x, [ax])
        self.y = np.append(self.y, [ay])
        self.w = np.append(self.w, [1.0])
        self.i += 1

    def remove_point(self, ind):
        self.x = np.delete(self.x, ind)
        self.y = np.delete(self.y, ind)
        self.w = np.delete(self.w, ind)
        self.i -= 1

    def change_color(self, c):
        self.color = c

    def change_thick(self, t):
        self.thick = t

    def show_curve(self):
        self.visibility = 1

    def cover_curve(self):
        self.visibility = 0

    def show_control_points(self):
        self.control_points = 1

    def cover_control_points(self):
        self.control_points = 0

    def shiftv(self, vx, vy):
        self.x = vx+self.x
        self.y = self.y+vy
        # print(self.x)
        # print(self.y)

    def edit_point(self, k, newx, newy):
        self.x[k] = newx
        self.y[k] = newy

    def swap_points(self, k, j):
        tx = self.x[k]
        ty = self.y[k]
        self.x[k] = self.x[j]
        self.y[k] = self.y[j]
        self.x[j] = tx
        self.y[j] = ty

    def change_type(self, k):
        if k < 8:
            self.type = k

    def change_weight(self, k, nw):
        self.w[k] = nw

    def scale(self, k):
        Xnew = np.array([self.x[0]])
        Ynew = np.array([self.y[0]])
        for j in range(1, self.i):
            Xnew = np.append(Xnew, [Xnew[j-1]+k*(self.x[j]-self.x[j-1])])
            Ynew = np.append(Ynew, [Ynew[j-1]+k*(self.y[j]-self.y[j-1])])
        self.x = Xnew
        self.y = Ynew

    def rotate(self, alpha):
        for j in range(0, self.i):
            ex = self.x[j]
            ey = self.y[j]
            self.x[j] = ex*math.cos(math.radians(alpha))-ey * \
                math.sin(math.radians(alpha))
            self.y[j] = ex*math.sin(math.radians(alpha))+ey * \
                math.cos(math.radians(alpha))
