import os 
os.chdir( "/home/anderson/Python-Scripts" ) #MTA ATENCAO AQUI: diretorio de trabalho!
import redesMutualisticas as nui #'redesMutualisticas.py' deve estar no dir de trabalho
import time
import pandas as pd

start_time = time.time()
mensagem = '||| Runing Nuismer Model |||'
print mensagem.center(100)
###########
###########

N = 200 #n inicial de individuos 
Sanimal = 5 #numero de sps 
Splants = 5 #numero de sps
offspring = 3 #prole
carringCapacity = 200 #capacidadae de suporte
alphaVector = [1.8]#[0.01,0.5,0.9] #lista para iterar
gammaVector = [0.5]#[0.01,0.5,0.9] 3lista para iterar
thetaAnimal = [10,20,30,40,50,60] #[rd.randint(10+Sanimal,50+Sanimal) for i in range(Sanimal)] #aleatorio
thetaPlants = [10,20,30,40,50,60] #[rd.randint(10+Splants,50+Splants) for i in range(Splants)] #aleatorio
eta = 5 #numero de visitas realizadas pelos animais (plantas ao acaso)
timeLen = 100 #tempo (ou numero de geracoes)

for alpha in alphaVector:
    for gamma in gammaVector:
        mymodel = nui.nuismerModel(N,Sanimal,Splants,offspring,carringCapacity,alpha,gamma,thetaAnimal,thetaPlants,eta,timeLen) #paratriza o modelo
        mymodel.run() #roda
        #salvando arquivos
        pd.DataFrame(mymodel.outputInteractionMatrix).to_csv('intMat'+str(alpha)+str(gamma)+'.csv') #matriz de interacao .csv
        pd.DataFrame(mymodel.outputPlantsPop).to_csv('plaPop'+str(alpha)+str(gamma)+'.csv') #abundancia de plantas .csv
        pd.DataFrame(mymodel.outputAnimalPop).to_csv('aniPop'+str(alpha)+str(gamma)+'.csv') #abundancia de animais .csv
        pd.DataFrame(mymodel.outputAnimalFenMean).to_csv('aniFenMean'+str(alpha)+str(gamma)+'.csv') #fenotipo medio das sps animais .csv
        pd.DataFrame(mymodel.outputAnimalFenSD).to_csv('aniFenSD'+str(alpha)+str(gamma)+'.csv') # SD do fenotipo de animais .csv
        pd.DataFrame(mymodel.outputPlantsFenMean).to_csv('plaFenMean'+str(alpha)+str(gamma)+'.csv') #fenotipo medio das sps plantas .csv
        pd.DataFrame(mymodel.outputPlantsFenMean).to_csv('plaFenSD'+str(alpha)+str(gamma)+'.csv') #SD do fenotipo de plantas .csv

###########
###########
print '\nTime: %s minutes\n'  % ((time.time()-start_time)/60)
