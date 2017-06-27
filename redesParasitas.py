import numpy as np
import matplotlib.pylab as pl

print "Rodando..."

##INFO##
#Estados humanos: 0=vazio; 1=individuo suceptivel; 2=individuo infectado; 3=individuo recuperado
#Estados vetores e reservatorios: 0=vazio; 1=ocupado-sp1; 2=ocupado-sp2; 3=ocupado-sp3

#lattice
dimensao = 50
nSps = 3
latHuman = np.random.randint(0,2,(dimensao, dimensao))
latVet = np.random.randint(0,2,(nSps,dimensao, dimensao))
latRes = np.random.randint(0,3,(nSps,dimensao, dimensao))
#lat=np.zeros((dimensao,dimensao))
#lat[25][25]=1


#parametros
it = 50 #numero de iteracoes
#tamanho populacional
Nhuman = [sum(latHuman>0)]
Nvet = [sum(latVet[i,:,:]>0) for i in range(nSps)]  #[sum(sum(latVet>0))]
Nres = [sum(latRes[i,:,:]>0) for i in range(nSps)]  #[sum(sum(latRes>0))]
#prevalencia infeccoes
prevHuman = [sum(latHuman==2)/sum(latHuman>0)]
prevVet = [sum(latVet[i,:,:]==2)/sum(latVet[i,:,:]>0) for i in range(nSps)]  #[sum(sum(latVet>0))]
prevRes = [sum(latRes[i,:,:]==2)/sum(latRes[i,:,:]>0) for i in range(nSps)]  #[sum(sum(latRes>0))]

#probsHuman = [1.0/nSps,2.0/nSps,3.0/nSps]
probsVetCompleta = np.ones((nSps,nSps)) #rede completamente conectada
probsVetAninhada = np.tril(np.ones(nSps)) #rede aninhada
probsVetCompart = np.eye(nSps) #rede compartimentalizada


def checaVizinhos(matriz, dimensao01, dimensao02, sp):
    x=matriz
    i=dimensao01
    j=dimensao02
    sp=sp
    outCheca=[]

    #checando as celulas vizinhas
    if i==0 and j==0:
        outCheca = [x[sp,i,j+1],x[sp,i+1,j]]
    elif i==(dimensao-1) and j==(dimensao-1):
        outCheca = [x[sp,i,j-1],x[sp,i-1,j]]
    elif i==0 and j==(dimensao-1):
        outCheca = [x[sp,i+1,j],x[sp,i,j-1]]
    elif i==(dimensao-1) and j==0:
        outCheca = [x[sp,i,j+1],x[sp,i-1,j]]
    elif i==0 and 0<j<(dimensao-1):
        outCheca = [x[sp,i,j+1],x[sp,i+1,j],x[sp,i,j-1]]
    elif 0<i<(dimensao-1) and j==0:
        outCheca = [x[sp,i,j+1],x[sp,i+1,j],x[sp,i-1,j]]
    elif i==(dimensao-1) and 0<j<(dimensao-1):
        outCheca = [x[sp,i,j+1],x[sp,i,j-1],x[sp,i-1,j]]
    elif 0<i<(dimensao-1) and j==(dimensao-1):
        outCheca = [x[sp,i+1,j],x[sp,i,j-1],x[sp,i-1,j]]
    elif 0<i<(dimensao-1) and 0<j<(dimensao-1):
        outCheca = [x[sp,i,j+1],x[sp,i+1,j],x[sp,i,j-1],x[sp,i-1,j]]

    return outCheca

def checaVizinhosHuman(matriz, dimensao01, dimensao02):
    x=matriz
    i=dimensao01
    j=dimensao02
    outCheca=[]

    #checando as celulas vizinhas
    if i==0 and j==0:
        outCheca = [x[i,j+1],x[i+1,j]]
    elif i==(dimensao-1) and j==(dimensao-1):
        outCheca = [x[i,j-1],x[i-1,j]]
    elif i==0 and j==(dimensao-1):
        outCheca = [x[i+1,j],x[i,j-1]]
    elif i==(dimensao-1) and j==0:
        outCheca = [x[i,j+1],x[i-1,j]]
    elif i==0 and 0<j<(dimensao-1):
        outCheca = [x[i,j+1],x[i+1,j],x[i,j-1]]
    elif 0<i<(dimensao-1) and j==0:
        outCheca = [x[i,j+1],x[i+1,j],x[i-1,j]]
    elif i==(dimensao-1) and 0<j<(dimensao-1):
        outCheca = [x[i,j+1],x[i,j-1],x[i-1,j]]
    elif 0<i<(dimensao-1) and j==(dimensao-1):
        outCheca = [x[i+1,j],x[i,j-1],x[i-1,j]]
    elif 0<i<(dimensao-1) and 0<j<(dimensao-1):
        outCheca = [x[i,j+1],x[i+1,j],x[i,j-1],x[i-1,j]]

    return outCheca

def transicaoPop(vetor,matriz,dimensao01,dimensao02,sp):
    VetorVizinhos = vetor
    outTrans = matriz
    i = dimensao01
    j = dimensao02
    sp = sp
    VizinhoEstados = [VetorVizinhos[k]==sp for k in range(len(VetorVizinhos))]
    
    if (outTrans[sp,i,j]==0):
        if sum(VizinhoEstados)>0:
            outTrans[sp,i,j] = 1
    else:
        outTrans[sp,i,j] = 0

    return outTrans

def transicaoPopHuman(vetor,matriz,dimensao01,dimensao02):
    VetorVizinhos = vetor
    outTrans = matriz
    i = dimensao01
    j = dimensao02
    VizinhoEstados = [VetorVizinhos[k]>0 for k in range(len(VetorVizinhos))]
    
    if (outTrans[i,j]==0):
        if sum(VizinhoEstados)>0:
            outTrans[i,j] = 1
    else:
        outTrans[i,j] = 0

    return outTrans

def transicaoInfec(lista,matriz,matrizProbs,dimensao01,dimensao02,sp,nivel):
    lista = lista
    outTrans = matriz
    matrizProbs = matrizProbs
    i = dimensao01
    j = dimensao02
    sp=sp
    nivel = nivel #se vetor ou reservatorio
    VizinhoEstados = [lista[k]==2 for k in range(len(lista))]

    if outTrans[sp,i,j]==1:
        if nivel=='vetor':
            probMediaInfec = np.mean( [matrizProbs[sp,j] for j in np.array([lista[i] for i in range(len(lista)) if lista[i]>0])-1] )
        else:
            probMediaInfec = np.mean( [matrizProbs[j,sp] for j in np.array([lista[i] for i in range(len(lista)) if lista[i]>0])-1] )
            
        if (sum(VizinhoEstados)>0) and (probMediaInfec>np.random.random()):
            outTrans[sp,i,j] = 2

    return outTrans

def transicaoInfecHuman(lista,matriz,matrizProbs,dimensao01,dimensao02):
    lista = lista
    outTrans = matriz
    matrizProbs = matrizProbs
    i = dimensao01
    j = dimensao02
    VizinhoEstados = [lista[k]==2 for k in range(len(lista))]

    if outTrans[i,j]==1:            
        if (sum(VizinhoEstados)>0):
            outTrans[sp,i,j] = 2

    return outTrans


####SIMULACOES####
for h in range(it):
    #tamanho populacional
    Nhuman.extend([sum(latHuman>0)])
    Nvet.extend([sum(latVet>0)])
    Nres.extend([sum(latRes>0)])
    #prevalencia
    prevHuman.extend([sum(latHuman==2)/sum(latHuman>0)])
    prevVet = np.vstack((prevVet,[sum(latVet[i,:,:]==2)/sum(latVet[i,:,:]>0) for i in range(nSps)]))
    prevRes = np.vstack((prevRes,[sum(latRes[i,:,:]==2)/sum(latRes[i,:,:]>0) for i in range(nSps)]))

    #rede de interacao vetor X reservatorio
    matrizProbs = probsVetCompleta
    
    randomi=randomj=range(dimensao)
    np.random.shuffle(randomi)
    np.random.shuffle(randomj)
    for i in range(nSps):
        for j in range(dimensao):
            for k in range(dimensao):
                posicaoj = randomi[j]
                posicaok = randomj[k]
                sp = i

                #dinamica pop
                vizinhosHuman = checaVizinhosHuman(latHuman,posicaoi,posicaoj)
                vizinhosVet = checaVizinhos(latVet,posicaoi,posicaoj,sp)
                vizinhosRes = checaVizinhos(latRes,posicaoi,posicaoj,sp)
                latHuman = transicaoPopHuman(vizinhosHuman,latHuman,posicaoi,posicaoj)
                latVet = transicaoPop(vizinhosVet,latVet,posicaoi,posicaoj,sp)
                latRes = transicaoPop(vizinhosRes,latRes,posicaoi,posicaoj,sp)

                #dinamica de infeccoes
                latHuman = transicaoInfecHuman(vizinhosVet,latHuman,matrizProbs,posicaoi,posicaoj)
                latVet = transicaoInfec(vizinhosRes,latVet,matrizProbs,posicaoi,posicaoj,sp,'vetor')

##Graficos
#Lattice
pl.imshow(lat,cmap='Greys',interpolation='nearest')
pl.show()
#N no tempo
#pl.plot(N)
#pl.show()
##

print "Rodou!"
