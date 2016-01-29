import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint 

def meueuler( f, x0, t ):
    n = len( t )
    x = np.array( [x0] * n )
    for i in xrange( n - 1 ):
        x[i+1] = x[i] + ( t[i+1] - t[i] ) * f( x[i], t[i] )

    return x

def model(state,t):
    x = state     
    a = 2
    b = 0.02
    c = 0.2
    d = 0.004
    k = 100

    return x*a*( 1 - x*k**-1 ) # corresponds to [dx/dt, dy/dt]

x0=20

t = np.linspace( 0, 100, 100000 )

result = meueuler( model, x0, t )
print result

plt.plot(t,result)
plt.show()
