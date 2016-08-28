import matplotlib.pyplot as plt
import numpy as np
#from pylab import *
#from scipy.integrate import odeint

def meurk4( f, x0, t ):
    n = len( t )
    x = np.array( [ x0 ] * n )    

    for i in xrange( n - 1 ):
        
        h = t[i+1] - t[i]
        
        k1 = h * f( x[i], t[i] )
        k2 = h * f( x[i] + 0.5 * k1, t[i] + 0.5 * h )
        k3 = h * f( x[i] + 0.5 * k2, t[i] + 0.5 * h )
        k4 = h * f( x[i] + k3, t[i+1])

        x[i+1] = x[i] + ( k1 + 2.0 * ( k2 + k3 ) + k4 ) * 6.0**-1

    return x

def model(state,t):
    x,y = state     
    a = 0.5
    b = 0.02
    c = 0.2
    d = 0.004
    k = 100

    return np.array([ x*(a*(1-x*k**-1)-y*b) , -y*(c - x*d) ]) # corresponds to [dx/dt, dy/dt]
###
#def model2(state,t):
#    x = state     
#    a = 0.9
#    b = 0.02
#    c = 0.2
#    d = 0.004
#    k = 600

 #   return x*a*( 1 - x*k**-1 ) # corresponds to [dx/dt, dy/dt]
#x0=200
##################

# initial conditions for the system
x0 = 50.0
y0 = 20.0

# vector of time
t = np.linspace( 0, 100, 1000 )

result = meurk4( model, [x0,y0], t )
print result

plt.plot(t,result)

plt.xlabel('Time')
plt.ylabel('Population Size')
plt.legend(('x (prey)','y (predator)'))
plt.title('Lotka-Volterra Model')
plt.show()
