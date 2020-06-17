import numpy as np
import math


def werner_algorithm(X, n):
    # print("werner done")
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


def ratBezier(t, a, b, X, w, n):
    u = (t-a)/(b-a)
    s = 0.0
    for i in range(0, n):
        s += X[i]*Rni(i, n, w, u)
    return s


def Rni(i, n, w, u):
    s = 0.0
    for j in range(0, n):
        s += w[j]*Bernstein(j, n-1, u)
    return w[i]*Bernstein(i, n-1, u)/s


def Bernstein(k, n, t):
    if n >= k and n >= 0 and k >= 0:
        return math.factorial(n) / (math.factorial(k) * math.factorial(n-k)) * t**k * (1-t)**(n-k)


def deCasteljau(t, a, b, X, Y, n):
    Wx = X
    Wy = Y
    u = (t-a)/(b-a)
    #u = (t-100)/100
    for k in range(1, n):
        Wxnew = np.array([])
        Wynew = np.array([])
        for i in range(0, n-k):
            Wxnew = np.append(Wxnew, [(1-u)*Wx[i]+u*Wx[i+1]])
            Wynew = np.append(Wynew, [(1-u)*Wy[i]+u*Wy[i+1]])
        Wx = Wxnew
        Wy = Wynew
    return Wx[0], Wy[0]


def deCasteljauleft(t, a, b, X, Y, n):
    Wx = X
    Wy = Y
    Xwyn = np.array([Wx[0]])
    Ywyn = np.array([Wy[0]])
    u = (t-a)/(b-a)
    for k in range(1, n):
        Wxnew = np.array([])
        Wynew = np.array([])
        for i in range(0, n-k):
            Wxnew = np.append(Wxnew, [(1-u)*Wx[i]+u*Wx[i+1]])
            Wynew = np.append(Wynew, [(1-u)*Wy[i]+u*Wy[i+1]])
        Wx = Wxnew
        Wy = Wynew
        Xwyn = np.append(Xwyn, [Wx[0]])
        Ywyn = np.append(Ywyn, [Wy[0]])
   # print(Xwyn)
   # print(Ywyn)
    return Xwyn, Ywyn


def deCasteljauright(t, a, b, X, Y, n):
    Wx = X
    Wy = Y
    Xwyn = np.array([Wx[n-1]])
    Ywyn = np.array([Wy[n-1]])
    u = (t-a)/(b-a)
    for k in range(1, n):
        Wxnew = np.array([])
        Wynew = np.array([])
        for i in range(0, n-k):
            Wxnew = np.append(Wxnew, [(1-u)*Wx[i]+u*Wx[i+1]])
            Wynew = np.append(Wynew, [(1-u)*Wy[i]+u*Wy[i+1]])
        Wx = Wxnew
        Wy = Wynew
        Xwyn = np.append(Xwyn, [Wx[n-1-k]])
        Ywyn = np.append(Ywyn, [Wy[n-1-k]])
    # print(Xwyn)
    # print(Ywyn)
    return Xwyn[::-1], Ywyn[::-1]


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


def OISF3(t, xk, yk, xkm1, ykm1, Mk, Mkm1):
    hk = xk-xkm1
    return (1/6 * Mkm1 * (xk-t)**3 + Mk*(t - xkm1)**3 / 6 + (ykm1 - Mkm1*hk*hk/6)*(xk-t) + (yk - Mk*hk*hk/6)*(t-xkm1))/hk


def deterMnofs3(X, Y, n):
    h = np.zeros(n+1)
    q = np.array([])
    u = np.array([])
    s = np.array([])
    q = np.append(q, [0])
    u = np.append(u, [0])
    s = np.append(s, [1])
   # hn=X[1]-X[0]
    # hnm1=X[n-1]=X[n-2]
    #dnm1 = ((Y[k+1]-Y[k])/hkp1 - (Y[k]-Y[k-1])/hk)*6/(hk+hkp1)
    for k in range(1, n-1):
        h[k] = X[k]-X[k-1]
        h[k+1] = X[k+1]-X[k]
        lk = h[k]/(h[k]+h[k+1])
        pk = lk*q[k-1]+2
        q = np.append(q, [(lk-1)/pk])
        s = np.append(s, [-lk*s[k-1]/pk])
        u = np.append(
            u, [(((Y[k+1]-Y[k])/h[k+1] - (Y[k]-Y[k-1])/h[k])*6/(h[k]+h[k+1]) - lk * u[k-1])/pk])
    t = np.zeros(n)
    v = np.zeros(n)
    t[n-1] = 1
    for k in range(n-2, 0, -1):
        t[k] = q[k]*t[k+1]+s[k]
        v[k] = q[k]*v[k+1]+u[k]
    M = np.zeros(n+1)
    hn = X[n-1]-X[n-2]
    hnp1 = X[1]-X[0]
    ln = hn/(hn+hnp1)
    dn = 6/(hn+hnp1)*((Y[1]-Y[n-1])/hnp1 - (Y[n-1] - Y[n-2])/hn)
    M[n-1] = (dn - (1-ln)*v[1] - ln * v[n-1])/(2 + (1-ln)*t[1]+ln*t[n-2])
    M[0] = M[n-1]
    for k in range(1, n-1):
        M[k] = v[k]+t[k]*M[n-1]
    # for k in range(n-2, 0, -1):
      #   M[k] = v[k]+t[k]*M[k+1]
    M[n] = M[1]
    return M


def Horner(X, n, u):
    hor = 0
    X = X[::-1]
    for x in X:
        hor = hor*u + x
    return hor


def Bezierpointvalue(t, a, b, X, Y, n):
    u = (t-a)/(b-a)
    Qx = np.array([])
    Qy = np.array([])
    for k in range(0, n):
        nok = math.factorial(n-1)/(math.factorial(n-1-k)*math.factorial(k))
        Qx = np.append(Qx, [X[k]*nok])
        Qy = np.append(Qy, [Y[k]*nok])
    if u <= 0.5:
        v = u/(1-u)
        return Horner(Qx, n-1, v)*(1-u)**(n-1), Horner(Qy, n-1, v)*(1-u)**(n-1)
    else:
        v = (1-u)/u
        Qx = Qx[::-1]
        Qy = Qy[::-1]
        return Horner(Qx, n-1, v)*(u)**(n-1), Horner(Qy, n-1, v)*(u)**(n-1)


def degup(X, Y, n):
    Xnew = np.array([X[0]])
    Ynew = np.array([Y[0]])
    for k in range(1, n):
        Xnew = np.append(Xnew, [k/n*X[k-1]+(1-k/n)*X[k]])
        Ynew = np.append(Ynew, [k/n*Y[k-1]+(1-k/n)*Y[k]])
    Xnew = np.append(Xnew, [X[n-1]])
    Ynew = np.append(Ynew, [Y[n-1]])
    return Xnew, Ynew


def degdown(X, Y, n):
    XI = np.array([X[0]])
    YI = np.array([Y[0]])
    XII = np.array([X[n-1]])
    YII = np.array([Y[n-1]])
    nhf = math.floor((n-1)/2)+1
    for k in range(1, nhf):
        XI = np.append(XI, [(1+k/(n-1-k))*X[k] - k/(n-1-k)*XI[k-1]])
        YI = np.append(YI, [(1+k/(n-1-k))*Y[k] - k/(n-1-k)*YI[k-1]])
    for k in range(1, math.ceil((n-1)/2)):
        XII = np.append(XII, [(n-1)/(n-1-k)*X[n-1-k] +
                              (1-(n-1)/(n-1-k))*XII[k-1]])
        YII = np.append(YII, [(n-1)/(n-1-k)*Y[n-1-k] +
                              (1-(n-1)/(n-1-k))*YII[k-1]])
    # print(np.size(XI))
    # print(np.size(XII))
    XII = XII[::-1]
    YII = YII[::-1]
    # print(XI)
    # print(XII)
    xs = 0.5*XI[math.floor((n-1)/2)] + 0.5*XII[0]
    ys = 0.5*YI[math.floor((n-1)/2)] + 0.5*YII[0]
    # print(xs)
    XI = np.delete(XI, math.floor((n-1)/2))
    XII = np.delete(XII, 0)
    YI = np.delete(YI, math.floor((n-1)/2))
    YII = np.delete(YII, 0)
    XI = np.append(XI, [xs])
    YI = np.append(YI, [ys])
    XI = np.append(XI, XII)
    YI = np.append(YI, YII)
    # print(XI)
    return XI, YI
