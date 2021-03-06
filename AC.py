import numpy as np
import matplotlib.pylab as pl

print "Rodando..."

##INFO##
#Estados: 0=vazio; 1=ocupado

#lattice
dimensao=50
#lat=g = np.floor(np.random.random((dimensao, dimensao)) + .5)
lat=np.zeros((dimensao,dimensao))
lat[25][25]=1


#parametros
it = 50 #numero de iteracoes
N=[sum(sum(lat))]
def checa(matriz, dimensao01, dimensao02):
    x=matriz
    i=dimensao01
    j=dimensao02
    outCheca=[]

    #checando as celulas vizinhas
    if i==0 and j==0:
        outCheca = [x[i][j+1],x[i+1][j]]
    elif i==(dimensao-1) and j==(dimensao-1):
        outCheca = [x[i][j-1],x[i-1][j]]
    elif i==0 and j==(dimensao-1):
        outCheca = [x[i+1][j],x[i][j-1]]
    elif i==(dimensao-1) and j==0:
        outCheca = [x[i][j+1],x[i-1][j]]
    elif i==0 and 0<j<(dimensao-1):
        outCheca = [x[i][j+1],x[i+1][j],x[i][j-1]]
    elif 0<i<(dimensao-1) and j==0:
        outCheca = [x[i][j+1],x[i+1][j],x[i-1][j]]
    elif i==(dimensao-1) and 0<j<(dimensao-1):
        outCheca = [x[i][j+1],x[i][j-1],x[i-1][j]]
    elif 0<i<(dimensao-1) and j==(dimensao-1):
        outCheca = [x[i+1][j],x[i][j-1],x[i-1][j]]
    elif 0<i<(dimensao-1) and 0<j<(dimensao-1):
        outCheca = [x[i][j+1],x[i+1][j],x[i][j-1],x[i-1][j]]

    return outCheca

def transicao(vetor,matriz,dimensao01,dimensao02):
    VetorVizinhos=vetor
    outTrans=matriz
    i=dimensao01
    j=dimensao02
    VizinhoEstados = [VetorVizinhos[k]==1 for k in range(len(VetorVizinhos))]

    if outTrans[i][j]==0:
        if sum(VizinhoEstados)>0:
            outTrans[i][j]=1
    else:
        outTrans[i][j]=0

    return outTrans

####SIMULACOES####
for h in range(it):
    N.extend([sum(sum(lat))])
    randomi=randomj=range(dimensao)
    np.random.shuffle(randomi)
    np.random.shuffle(randomj)
    for i in range(dimensao):
        for j in range(dimensao):
            posicaoi=randomi[i]
            posicaoj=randomj[j]
            
            vizinhos=checa(lat,posicaoi,posicaoj)
            lat=transicao(vizinhos,lat,posicaoi,posicaoj)


##Graficos
#Lattice
#pl.imshow(lat,cmap='Greys',interpolation='nearest')
#pl.show()
#N no tempo
#pl.plot(N)
#pl.show()
##

print "Rodou!"
