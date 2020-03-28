import numpy as np

# types:
# 1. polyline


class Curve:
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])
        self.color = 'blue'
        self.thick = 1
        self.control_points = 1
        self.visibility = 1
        self.type = 1
        self.i = 0  # liczba punktow

    def add_point(self, ax, ay):
        self.x = np.append(self.x, [ax])
        self.y = np.append(self.y, [ay])
        self.i += 1

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
        self.x = self.x+vx
        self.y = self.y+vy

    def edit_point(self, k, newx, newy):
        self.x[k] = newx
        self.y[k] = newy

    def rev_order(self, k, j):
        tx = self.x[k]
        ty = self.y[k]
        self.x[k] = self.x[j]
        self.y[k] = self.y[j]
        self.x[j] = tx
        self.y[j] = ty
