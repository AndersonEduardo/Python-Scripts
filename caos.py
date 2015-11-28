from numpy import *
import pylab as pl
##
Print 'Processando...'
##
##Parametrizacao
Nmap=[]
K=100
r=linspace(0,3,500)
rmap=[]
tempo=50

##Simulacoes
for h in range(len(r)):
    N = [10] #[random.randint(1,10)]
    for i in range(tempo):
        if N[0]<=0:
            break
        else:
            N.append(N[i] + N[i]*r[h]*(1-N[i]*K**(-1)))

    Nmap.append(N[-25:])
    rmap.append([r[h]]*25)

##Grafico
pl.plot(rmap, Nmap, '.', c='black', ms=1)
pl.xlabel('r')
pl.ylabel('N')
pl.title('Mapa logistico')
pl.grid(True)
pl.show()

##
print 'Rodou!'
##
