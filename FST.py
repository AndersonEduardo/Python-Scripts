##
#Calculando indice de fixacao (FST) (BASE: Hudson, Slatkin, Maddison (1992) Estimation of Levels of Gene Flow from DNA Sequence Data).
#ParametroA = lista contendo duas sublistas com os alelos das populacoes (cada sublista e de uma populacao).
#Este codigo e capaz de comparar apenas uma par de populacoes de cada vez.
##
import random as rd
import numpy as np

def FST(parametroA, parametroB):
    comparacoes=[]
    dados = parametroA #[[1,1,1,1,1,1],[4,4,2,2,3,3]]

    for i in range(parametroB):
        a=rd.sample(dados[0],1)
        b=rd.sample(dados[1],1)
        if a==b:
            comparacoes.append(0)
        else:
            comparacoes.append(1)

    piEntrePop = np.mean(comparacoes)
    ##
    comparacoes=[]
    piDentroPopVetor=[]
    piDentroPop=[]
    for i in range(len(dados)):
        for j in range(parametroB):
            a1=rd.sample(dados[i],1)
            a2=rd.sample(dados[i],1)
            if a1==a2:
                comparacoes.append(0)
            else:
                comparacoes.append(1)

        piDentroPopVetor.append(np.mean(comparacoes))
    piDentroPop.append(np.mean(piDentroPopVetor))
    
    FSTvalor = (piEntrePop-piDentroPop)*(piEntrePop)**-1 #0=sem diferenciacao, 1=completa diferenciacao
    FSTvalor = abs(FSTvalor) #para evitar resultados negativos em razao de erro numerico

    return FSTvalor
