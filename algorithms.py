import numpy as np
import math


def werner_algorithm(X, n):
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
    for i in range(0, n-1):
        s += X[i]*Bernstein(i, n, u)
    return s


def Bernstein(k, n, t):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n-k)) * t**k * (1-t)**(n-k)
