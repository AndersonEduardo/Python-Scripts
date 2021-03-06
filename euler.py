import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint 

def meueuler( f, x0, t ):
    n = len( t )
    x = np.array([x0] * n)
    for i in xrange( n - 1 ):
        x[i+1] = x[i] + ( t[i+1] - t[i] ) * f( x[i], t[i] )

    return x

def model2(state,t):
    x = state     
    a = 1.1
    b = 0.02
    c = 0.2
    d = 0.004
    k = 100.0

    return x*a*( 1 - x/k ) # corresponds to [dx/dt, dy/dt]

x0 = 10.0

t = np.linspace( 0, 100, 100000 )

result = meueuler( model2, x0, t )
print result

plt.plot(t,result)
plt.show()