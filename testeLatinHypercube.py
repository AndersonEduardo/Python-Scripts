from pyDOE import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.stats.distributions import norm


# hipercubo latino

parsN = 2 #numero de parametros do modelo
replicasN = 5
hipercubo = lhs(parsN, samples=replicasN) #hipercubo latino
maxminPars = np.array([[0,3],[50,100]]) #range para amostragem de cada parametro
hipercuboOutput = []

for i in xrange(parsN):
    hipercubo[:, i] = np.random.uniform(maxminPars[i][0],maxminPars[i][1],replicasN) * hipercubo[:, i]

    
# modelo

def model2(state,t,r,k):
    n = state     
    #r = 1.7
    #k = 100

    return n*r*( 1 - n*k**-1 ) # corresponds to [dx/dt, dy/dt]


# usando o hipercubo no modelo

n0=20
t = np.linspace( 0, 1000, 100000 )

for r,k in hipercubo:   
    result = odeint( model2, n0, t, args=(r, k) )
    hipercuboOutput.append( [r, k, np.mean(result[len(result)/2 : len(result)-1]), np.std(result[len(result)/3 : len(result)-1]) ] )
        

# graficos
        
hipercuboOutputArray = np.asarray(hipercuboOutput)

plt.scatter(hipercuboOutputArray[:,0], hipercuboOutputArray[:,2], c='blue') #tamanho medio & r
plt.show()

plt.scatter(hipercuboOutputArray[:,0], hipercuboOutputArray[:,3], c='blue') #variancia & r
plt.show()

plt.scatter(hipercuboOutputArray[:,1], hipercuboOutputArray[:,2], c='red') #tamano medio & k
plt.show()

plt.scatter(hipercuboOutputArray[:,1], hipercuboOutputArray[:,3], c='red') #variancia & k
plt.show()
