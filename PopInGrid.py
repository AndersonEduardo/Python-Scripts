from numpy import *
import matplotlib.pyplot as pl

##Parameters and variables
N=zeros(shape=(10,10))+10
r=1 #2.821 #caotic dynamics for this last one
k=100
tempo=50
alfa=0.2

##Equations
for t in range(tempo):
    for i in range(10):
        for j in range(10):
            if i==0 and j==0:
                imigration=alfa*(N[i+1][j]+N[i][j+1])
                emigration=alfa*(N[i+1][j]+N[i][j+1])
            elif i==0 and 9>j>0:
                imigration=alfa*(N[i+1][j]+N[i][j+1]+N[i][j-1])
                emigration=alfa*(N[i+1][j]+N[i][j+1]+N[i][j-1])
            elif i==9 and 9>j>0: 
                imigration=alfa*(N[i-1][j]+N[i][j+1]+N[i][j-1])
                emigration=alfa*(N[i-1][j]+N[i][j+1]+N[i][j-1])
            elif 9>i>0 and j==0:
                imigration=alfa*(N[i+1][j]+N[i-1][j]+N[i][j+1])
                emigration=alfa*(N[i+1][j]+N[i-1][j]+N[i][j+1])
            elif 9>i>0 and j==9:
                imigration=alfa*(N[i+1][j]+N[i-1][j]+N[i][j-1])
                emigration=alfa*(N[i+1][j]+N[i-1][j]+N[i][j-1])
            elif i==9 and j==9:
                imigration=alfa*(N[i-1][j]+N[i][j-1])
                emigration=alfa*(N[i-1][j]+N[i][j-1])

            N[i][j] = N[i][j]+r*N[i][j]*(1-(N[i][j]+imigration-emigration)*k**-1)

## Set up a regular grid
xi, yi = arange(10), arange(10)
xi, yi = meshgrid(xi, yi)
zi = N

##Graphics
pl.imshow(zi, vmin=N.min(), vmax=N.max(), origin='lower')
pl.colorbar()
pl.show()

##
print 'Rodou!'
##
