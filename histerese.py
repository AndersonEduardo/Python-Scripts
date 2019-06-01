import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

def meueuler( f, x0, t, par ):
    n = len(t)
    x = np.array([x0] * n)
    for i in range(n - 1):
        x[i+1] = x[i] + (t[i+1] - t[i]) * f(x[i], t[i], par)

    return x

def histerese(mod, solv, x0, t, parRange):
    definedModel = mod
    definedSolver = solv
    x = x0
    time = t
    parRange = parRange
    histOut = []

    for par_i in parRange:
        histCalc = definedSolver(definedModel, x, time, par_i)
        x = histCalc[len(histCalc)-1]
        histOut.append(x)

    return histOut

def model(state, t, par):
    x = state
    a = par
    k = 100.0

    return x*a*( 1 - x/k ) # corresponds to [dx/dt, dy/dt]


x0 = 10.0
t = np.linspace( 0, 100, 100000 )
a = np.linspace(0.0,2.0,30)

res = histerese(model, meueuler, x0, t, a)

plt.plot(a,res)
plt.show()