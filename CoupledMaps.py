import numpy as np
import matplotlib.pylab as pl

###CAP: BEF E PAISAGENS###
from scipy.integrate import odeint 
from scipy import zeros_like
import matplotlib.pyplot as pl
##import os  #atencao aqui: NAO USAR IMPORT * !!! Usar soh import os e usar os.chdir... la em baixo.. 
from numpy import *
import random as rd
import scipy.integrate
import pandas as pd
import time as tm
import math
import string

print 'Rodando...'
print 'Hora do inicio: %s' %(tm.strftime('%d-%m-%Y %H:%M:%S'))

NumMaxPlantas=1 #numero maximo de especies de plantas
NumMaxFrag=1 #numero maximo de fragmentos
NumMaxGen=1 #numero maximo de genotipos
NumMaxConec=5 #numero de cenarios de conectividade
Nitera=1 #numero de iteracoes

mediaPlantas = []
SDPlantas = []
plantas=[]

numSPit=[]
numSPmedIt=[]
numPOPit=[]
numGENit=[]
numFUNCit=[]
numFRAGit=[]
grauCONECit=[]
SimpsonMedIt=[]
SimpsonSDit=[]
SimpsonPaisagemIt=[]
biomassaMedFragIt=[]
biomassaSDFragIt=[]
biomassaPaisagemIt=[]
numSP=[]
numSPmed=[]
numGEN=[]
numFUNC=[]
numFRAG=[]
grauCONEC=[]
biomassaMedFrag=[]
biomassaSDFrag=[]
biomassaPaisagem =[]
rho0=linspace(0,0.5,NumMaxConec)
SimpsonMed=[]
SimpsonSD=[]
SimpsonPaisagem=[]

for lconec in range(0,NumMaxConec): #loop para variar o grau de conectividade entre fragmentos
##for lgen in range(1,NumMaxGen+1): #lfra = loop sobre o numero de genotipos
    for lspp in range(1,NumMaxPlantas+1): #lfra = loop sobre o numero de sp de plantas
        for lfra in range(1,NumMaxFrag+1): #lsph = loop sobre o numero de especies de fragmentos
        #for lredun in range(1,lspp+1):
            solucoes=[]
            tabSolucoes=[]
            for it in range(0,Nitera): #Nitera = numero maximo de iteracoes
                #DEFININDO AS VARIAVEIS
                time = linspace(0,1000,10000) #tempo
                spp = lspp #random.randint(1,NumMaxPlantas+1) #numero de especies de plantas                        
                frag = 5#lfra #numero de fragmentos  
                #gen = 1 #numero de genotipos
                #SPredun = lredun #numero de grupos funcionais
                conec = lconec
                b=1 #taxa de conversao de biomassa viva (de plantas) em morta
                Rzero=50
                Vr=10
                #Vp=Vr*spp**-1

                ##variabilidade na complementaridade de nicho
                if spp<=5:
                    numGF=random.randint(1,spp+1)
                else:
                    numGF=random.randint(1,6)

                ##Vp correto sem genotipos
                VpBase=10
                letras=list(string.letters)
                Vp0=[]
                VpX=[]

                Vp0=letras[:numGF]
                Vp0.extend(random.choice(Vp0[:numGF],(spp-numGF)))

                VpGF=[]
                for i in range(spp):
                    x=[Vp0[i]==ravel(Vp0)]
                    VpGF.extend([sum(x)])

                Vp=[]

                for i in range(frag):
                    Vp3=[]
                    x=[]
                    for j in range(len(VpGF)):
                        x.extend([VpBase*VpGF[j]**-1])
                    Vp.append(x)
                ##FIM

                rP=0.02                
                K=10  ###ATENCAO: PRECISA SER MAIUSCULO AQUI! ###
                q=0.05
                lP=0.02
                
                if frag==1:
                    capa = 0
                    rho = 0
                else:
                    rho = rho0[conec] #4 #output de biomassa para outras sub-populacoes
                    capa = rho*(frag-1)**-1 #input de biomassa de outras sub-populacoes

                ##vetor de condicoes iniciais das variaveis##                                
                y0=[] 
                y0.extend([10]*frag)
                y0.extend([1]*frag*spp)
                y0.extend([1]*frag*spp)
                ##
                
                a=1
                
                #DEFININDO A FUNCAO
                def befmodel(y,t=0): #args=(param,)
                    dy=zeros_like(y)
                    
                    #DEFININDO AS 'N' EQUACOES DO MODELO
                    for i in range(0,frag): #loop para fragmentos de habitat
                        for j in range(0,spp): #loop para especies de plantas                            

                                li = frag + spp*i + j 
                                pi = frag + spp*frag + spp*i + j                                                                                                                                                  
                                primeiroLdoFrag = frag + spp*i
                                ultimoLdoFrag = frag + spp*i + spp

                                primeiroPdoFrag = frag + spp*frag + spp*i
                                ultimoPdoFrag = frag + spp*frag + spp*i + spp

                                ##Calculando a biomassa da especie no fragmento vizinho
                                if i==0:
                                    biomassaDaSpNaPaisagem = rho* y[frag + spp*frag + spp*(i+1) + j]
                                    emigracao = rho*y[pi]
                                elif i==(frag-1):
                                    biomassaDaSpNaPaisagem = rho*y[frag + spp*frag + spp*(i-1) + j]
                                    emigracao = rho*y[pi]
                                else:
                                    biomassaDaSpNaPaisagem = rho*(y[frag + spp*frag + spp*(i+1)] + y[frag + spp*frag + spp*(i-1) + j])
                                    emigracao = 2*rho*y[pi]

                                ##Equacoes do modelo
                                dy[pi] = a*y[li]*y[pi] - b*y[pi] + biomassaDaSpNaPaisagem - emigracao
                                dy[li] = K*(y[i]-y[li]) - (a*Vp[i][j]**-1)*y[li]*y[pi]  
                                dy[i] = q*(Rzero-y[i]) - sum( (ravel(Vp[i])*Vr**-1)*K*(y[i]-y[primeiroLdoFrag:ultimoLdoFrag]) ) + sum( (1-lP)*b*(1*Vr**-1)*y[primeiroPdoFrag:ultimoPdoFrag] ) 
                                                           
                    return dy #array([dR,dL,dP,dH,dY,dDP,dDH,dDY])
            
    #RODANDO A INTEGRACAO NUMERICA PARA O SISTEMA DE EQUACOES
            
                y = odeint(befmodel, y0, time)  #args=(param,) #, Dfun = befmodel

                solucoes=y[len(y)-1] #pontos fixos das equacoes
                testeExtincao=sum([solucoes[i]<1e-10 for i in range(len(solucoes))])
                if testeExtincao >= 1:
                    print 'Extincao!'
                testeExplosao=sum([solucoes[i]>1e+10 for i in range(len(solucoes))])
                if testeExplosao >= 1:
                    print 'Explodiu! Boommm!'
                numSPit.extend([spp])
                numFUNCit.extend([numGF])                        
                numFRAGit.extend([frag])
                grauCONECit.extend([rho])
                #biomassaMedFragIt.append(sum(solucoes[frag + spp*frag:])*frag**-1) #obtendo a biomassa media nos fragmetos
                biomassaPaisagemIt.append(sum(solucoes[frag + spp*frag:])) #obtendo a biomasa na paisagem
                Simpson=[]
                biomassaFragMeanHelper=[]
                for i in range(0,frag): #loop para fragmentos de habitat                
                    primeiroPdoFrag = frag + spp*frag + spp*i
                    ultimoPdoFrag = frag + spp*frag + spp*i + spp
                    biomassaFragHelper=sum(solucoes[primeiroPdoFrag:ultimoPdoFrag])
                    biomassaFragMeanHelper.append(biomassaFragHelper)
                    Simpson.extend([solucoes[primeiroPdoFrag:ultimoPdoFrag].max()*biomassaFragHelper**-1]) #BERGER-PARKER
                    #Simpson.extend([sum(solucoes[primeiroPdoFrag:ultimoPdoFrag]*biomassaFragHelper**-1)**2])
                biomassaMedFragIt.append(mean(biomassaFragMeanHelper))
                biomassaSDFragIt.append(std(biomassaFragMeanHelper))
                SimpsonMedIt.extend([mean(Simpson)])
                SimpsonSDit.extend([std(Simpson)])
                SimpsonPaisagemIt.extend([solucoes[frag + spp*frag:].max()*(sum(solucoes[frag + spp*frag:]))**-1]) #BERGER-PARKER

            numSP.extend(numSPit)
            numGEN.extend(numGENit)
            numFUNC.extend(numFUNCit)
            numFRAG.extend(numFRAGit)
            grauCONEC.extend(grauCONECit)
            SimpsonMed.extend(SimpsonMedIt)
            SimpsonSD.extend(SimpsonSDit)
            SimpsonPaisagem.extend(SimpsonPaisagemIt)
            biomassaMedFrag.extend(ravel(biomassaMedFragIt))
            biomassaSDFrag.extend(biomassaSDFragIt)
            biomassaPaisagem.extend(ravel(biomassaPaisagemIt))

dadosCAP3 = pd.DataFrame([numSP,numFUNC,numFRAG,grauCONEC,SimpsonMed,SimpsonSD,SimpsonPaisagem,biomassaMedFrag,biomassaSDFrag,biomassaPaisagem])
dadosCAP3 = pd.DataFrame.transpose(dadosCAP3)
dadosCAP3.columns = ['NumSP','NumFUNC','NumFRAG','GrauCONEC','SimpsonMed','SimpsonSD','SimpsonPaisagem','massaMedFRAG','massaSdFRAG','massaPAIS']
#os.chdir('/home/anderson')
#savetxt('dadosCAP3.csv',dadosCAP3)

print 'cOwAbuNGa!! RODOU mAnO!!'
print 'Hora do fim: %s' %(tm.strftime('%d-%m-%Y %H:%M:%S'))
