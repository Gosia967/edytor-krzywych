import numpy as np
import math


def werner_algorithm(X, n):
    #print("werner done")
    # X is array of n+1 points
    A = [[0] * (n) for i in range(n)]
    A[0][0] = 1
    for j in range(1, n):
        A[j][0] = 0
    for i in range(1, n):
        for k in range(0, i):
            A[k][i] = A[k][i-1]/(X[k]-X[i])
            A[i][k+1] = A[i][k]-A[k][i]
    W = np.array([])
    for i in range(0, n):
        W = np.append(W, [A[i][n-1]])
    return W


def Lagrange(t, X, Y, n):
    W = werner_algorithm(X, n)
    s = 0
    for i in range(0, n):
        p = 1
        for j in range(0, n):
            if j != i:
                p *= t-X[j]
        s += W[i]*Y[i]*p
    return s


def Bezier(t, a, b, X, n):
    u = (t-a)/(b-a)
    s = 0
    for i in range(0, n):
        s += X[i]*Bernstein(i, n-1, u)
    return s


def Bernstein(k, n, t):
    if n >= k and n >= 0 and k >= 0:
        return math.factorial(n) / (math.factorial(k) * math.factorial(n-k)) * t**k * (1-t)**(n-k)


def NISF3(t, xk, yk, xkm1, ykm1, Mk, Mkm1):
    hk = xk-xkm1
    return (1/6 * Mkm1 * (xk-t)**3 + Mk*(t - xkm1)**3 / 6 + (ykm1 - Mkm1*hk*hk/6)*(xk-t) + (yk - Mk*hk*hk/6)*(t-xkm1))/hk


def deterMnifs3(X, Y, n):
    q = np.array([])
    u = np.array([])
    q = np.append(q, [0])
    u = np.append(u, [0])
    for k in range(1, n-1):
        hk = X[k]-X[k-1]
        hkp1 = X[k+1]-X[k]
        lk = hk/(hk+hkp1)
        pk = lk*q[k-1]+2
        q = np.append(q, [(lk-1)/pk])
        u = np.append(
            u, [(dk3(X[k-1], X[k], X[k+1], Y[k-1], Y[k], Y[k+1])*6 - lk * u[k-1])/pk])
    M = np.zeros(n)
    M[n-2] = u[n-2]
    for k in range(n-3, 0, -1):
        M[k] = u[k]+q[k]*M[k+1]
    return M


def dk3(x0, x1, x2, y0, y1, y2):
    return y0/(x0-x1)/(x0-x2)+y1/(x1-x0)/(x1-x2)+y2/(x2-x1)/(x2-x0)
