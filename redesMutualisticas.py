import numpy as np
import random as rd
import matplotlib.pyplot as pl
import pandas as pd
import sys

class organisms(object):
    def __init__(self,group,sp,fen,offs,age):
        self.group = group
        self.sp = sp #definindo a especie do organismo
        self.fen = fen #definindo seu genotipo
        self.offspring = offs 
        self.statusLife = 1 #definindo se esta vivo
        self.age = age

class environment(object):
    def __init__(self,offs,alpha,gamma,theta,carringCapacity):
#        self.population = [] #array de populacoes
        # self.abundancePlants = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        # self.abundanceAnimal = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        # self.plantsFenDataList = []
        # self.animalFenDataList = []
#        self.numInd = N #definindo o numero de individuos no ambiente
        # self.numSpAn = Sanimal #definindo o numero de especies animais
        # self.numSpPlan = Splants #definindo o numero de especies plantas
        self.offspring = offs 
        self.alpha = alpha
        self.gamma = gamma
        self.theta = theta
        self.carringCapacity = carringCapacity

    def criatePop(self,group,N,sp):
        self.group = group
        self.numInd = N
        self.numSp = sp
        self.popNew = []
        for i in range(self.numSp): #loop sobre numero de especies
            self.sp_i = []
            for j in range(self.numInd): #loop sobre o numero de individuos
                self.sp_i.append(organisms(self.group,i,self.theta + np.random.uniform(-self.theta,self.theta),self.offspring,0))
            self.popNew.append(self.sp_i) #add o novo organismo no final do array de organismos
        return self.popNew

    def animalReproduction(self,popAni,popPlan,nSp,intMat): #reproducao assexuada (depende apenas da interacao)
        self.animalsPop = popAni
        self.plantsPop = popPlan
        self.numSp = nSp
        self.interactionMatrix = intMat
        if len(np.concatenate(self.plantsPop)) == 0:
            print "\n !!!The network collapsed!!! \n"
        for i in range(self.numSp):
            for j in range(len(self.animalsPop[i])):
                if (self.animalsPop[i][j].age > 0):
                    #obtendo valor da funcao para prob. de interacao
                    self.Za = self.animalsPop[i][j].fen
                    self.intPar = np.concatenate(self.plantsPop)[rd.randint(0,len(np.concatenate(self.plantsPop))-1)] 
                    self.Zp = self.intPar.fen
                    self.indIntProb = self.interaction(self.Za,self.Zp,self.alpha) 

                    if self.indIntProb > np.random.uniform():
                        self.indFitness = self.fitness(self.animalsPop[i][j].fen,self.gamma,self.theta)
                        self.interactionMatrix[self.animalsPop[i][j].sp][self.intPar.sp] += 1 #atualizando a matriz de interacao

                        if self.indFitness > np.random.uniform():
                            for i_Offsp in range(self.animalsPop[i][j].offspring): #add prole recursivamente para haver variabilidade em Fen.
                                self.animalsPop[i].extend([organisms('A',self.animalsPop[i][j].sp,self.animalsPop[i][j].fen+np.random.normal(0,self.theta),self.animalsPop[i][j].offspring,0)]) #adicionando novos inds na populacao.
        return self.animalsPop, self.interactionMatrix

    def plantsReproduction(self,popPlan,popAni,nSp,intMat): #reproducao assexuada (depende apenas da interacao)
        self.plantsPop = popPlan
        self.animalsPop = popAni
        self.numSp = nSp
        self.interactionMatrix = intMat
        if len(np.concatenate(self.animalsPop)) == 0:
            print "\n !!!The network collapsed!!! \n"
        for i in range(self.numSp):
            for j in range(len(self.plantsPop[i])):
                if (self.plantsPop[i][j].age > 0):
                    #obtendo valor da funcao para prob. de interacao
#                    self.Za = self.animalsPop[rd.randint(0,len(self.animalsPop)-1)][].fen
                    self.intPar = np.concatenate(self.animalsPop)[rd.randint(0,len(np.concatenate(self.animalsPop))-1)]
                    self.Za = self.intPar.fen
                    self.Zp = self.plantsPop[i][j].fen
                    self.indIntProb = self.interaction(self.Za,self.Zp,self.alpha) 

                    if self.indIntProb > np.random.uniform():
                        self.indFitness = self.fitness(self.plantsPop[i][j].fen,self.gamma,self.theta)
                        self.interactionMatrix[self.intPar.sp][self.plantsPop[i][j].sp] += 1 #atualizando a matriz de interacao

                        if self.indFitness > np.random.uniform():
                            for i_Offsp in range(self.plantsPop[i][j].offspring): #add prole recursivamente para haver variabilidade em Fen.
                                self.plantsPop[i].extend([organisms('P',self.plantsPop[i][j].sp,self.plantsPop[i][j].fen+np.random.normal(0,self.theta),self.offspring,0)]) #adicionando novos inds na populacao.
        return self.plantsPop, self.interactionMatrix

    def carringCapacityFunction(self,pop,nSp,k):
        self.pop = pop
        self.numSp = nSp
        self.carringCapacity = k
        self.updatedPop = []
        self.totalPop = np.concatenate(self.pop)

        for i in range(self.numSp):
            rd.shuffle(self.pop[i])
            self.updatedPop.append(self.pop[i][:self.carringCapacity])
        
        # rd.shuffle(self.totalPop)
        # self.totalPop = self.totalPop[:self.carringCapacity]
        # for i in range(self.numSp):
        #     self.updatedPop.append([x for x in self.totalPop if x.sp == i])
        return self.updatedPop
                
    def interaction(self,Za,Zp,alpha): #funcao para prob. de interacao (Nuismer et al. 201..)
        self.fZaZp = 1.0 / ( 1.0+np.exp(-alpha*(Za-Zp)) )
        return self.fZaZp

    def fitness(self,Zy,gamma,theta): #funcao para o fitness de cada organismo (Nuismer et al. 201..)
        self.wZy = np.exp(-gamma*(Zy-theta)**2)
        return self.wZy

    def updateAge(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        for i in range(self.numSp):
#            print [x.sp for x in np.concatenate(self.pop)], i
            for orgnsm in self.pop[i]:
                orgnsm.age+=1
#            print [x.sp for x in np.concatenate(self.pop)], i
        return self.pop 

    def death(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        self.updatedPop = []
        for i in range(self.numSp):
            for orgnsm in self.pop[i]:
                if orgnsm.age >=1:
#                    print orgnsm.age,orgnsm.statusLife
                    orgnsm.statusLife = 0
#                    print orgnsm.age,orgnsm.statusLife
            self.updatedPop.append([x for x in self.pop[i] if x.statusLife == 1])
        return self.updatedPop
    
    def updateAbundancesData(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        self.abundance = []
        for i in range(self.numSp): #loop sobre cada especie animal
#            self.counting = len(pop[i]) #len([x for x in self.pop if (x.sp == i)]) #contando quantos existem
            self.abundance.append(len(self.pop[i])) #registrando na variavel 'abundanciaAnimal'
#        self.abundanceArray = np.array(self.abundance) #transformando em 'array' (para o 'split')
#        self.abundanceSplit = np.split(self.abundanceArray,len(self.abundance)/(self.numSp)) #dividindo o array
#        self.abundanceData = pd.DataFrame(self.abundanceSplit) #transformando em 'array' em 'dataframe'
        return self.abundance

    def updataFenData(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        self.fenMean = []
        self.fenSD = []
        self.fenData = []
        for i in range(self.numSp):
            self.fenList = [x.fen for x in self.pop[i]]
            self.fenMean.extend([np.mean(self.fenList)])
            self.fenSD.extend([np.std(self.fenList)])
        return self.fenMean,self.fenSD

class nuismerModel:
    def __init__(self,N,Sanimal,Splants,offs,carringCapacity,alpha,gamma,theta,time):        
        self.N = N
        self.Sanimal = Sanimal
        self.Splants = Splants
        self.offspring = offs
        self.carringCapacity = carringCapacity
        self.alpha = alpha
        self.gamma = gamma
        self.theta = theta
        self.time = time
        self.modelObject = environment(self.offspring,self.alpha,self.gamma,self.theta,carringCapacity)
            
    def run(self):
        #variaveis
        self.abundancePlants_t = []
        self.abundanceAnimals_t = []
        self.fenPlantsMean_t = []
        self.fenAnimalsMean_t = []
        self.fenPlantsSD_t = []
        self.fenAnimalsSD_t = []
        self.interactionMatrix = np.zeros([self.Sanimal,self.Splants])
        #criando populacoes
        self.popPlants = self.modelObject.criatePop('P',self.N,self.Splants)
        self.popAnimals = self.modelObject.criatePop('A',self.N,self.Sanimal)
        #registrando dados de abundancia no tempo t=zero
        self.abundancePlants_t.append(self.modelObject.updateAbundancesData(self.popPlants,self.Splants))
        self.abundanceAnimals_t.append(self.modelObject.updateAbundancesData(self.popAnimals,self.Sanimal))
        #registrando dados de fenotipo no tempo t=zero
        self.fenPlantsCalc = self.modelObject.updataFenData(self.popPlants,self.Splants)
        self.fenPlantsMean_t.extend([self.fenPlantsCalc[0]])
        self.fenPlantsSD_t.extend([self.fenPlantsCalc[1]])
        self.fenAnimalsCalc = self.modelObject.updataFenData(self.popAnimals,self.Sanimal)
        self.fenAnimalsMean_t.extend([self.fenAnimalsCalc[0]])
        self.fenAnimalsSD_t.extend([self.fenAnimalsCalc[1]])
        #dinamica do modelo
        for t in range(self.time):
            #atualizando idade
            self.popPlants = self.modelObject.updateAge(self.popPlants,self.Splants)
            self.popAnimals = self.modelObject.updateAge(self.popAnimals,self.Sanimal)
            #capacidade de suporte
            self.popPlants = self.modelObject.carringCapacityFunction(self.popPlants,self.Splants,self.carringCapacity)
            self.popAnimals = self.modelObject.carringCapacityFunction(self.popAnimals,self.Sanimal,self.carringCapacity)
            #reproducao
            self.animalRep_t =  self.modelObject.animalReproduction(self.popAnimals,self.popPlants,self.Sanimal,self.interactionMatrix)
            self.popAnimals = self.animalRep_t[0]
            if t < int(0.5*self.time):
                self.interactionMatrix = np.zeros([self.Sanimal,self.Splants])
            else:
                self.interactionMatrix = self.animalRep_t[1]
            self.plantsRep_t = self.modelObject.plantsReproduction(self.popPlants,self.popAnimals,self.Splants,self.interactionMatrix)
            self.popPlants = self.plantsRep_t[0]
            if t < int(0.5*self.time):
                self.interactionMatrix = np.zeros([self.Sanimal,self.Splants])
            else:
                self.interactionMatrix = self.plantsRep_t[1]
            #morte
            self.popPlants =  self.modelObject.death(self.popPlants,self.Splants)
            self.popAnimals = self.modelObject.death(self.popAnimals,self.Sanimal)
            #registrando abundancias no tempo t
            self.abundanceAnimals_t.append(self.modelObject.updateAbundancesData(self.popAnimals,self.Sanimal))
            self.abundancePlants_t.append(self.modelObject.updateAbundancesData(self.popPlants,self.Splants))
            #registrando fenotipos no tempo t
            self.fenPlantsCalc = self.modelObject.updataFenData(self.popPlants,self.Splants)
            self.fenPlantsMean_t.extend([self.fenPlantsCalc[0]])
            self.fenPlantsSD_t.extend([self.fenPlantsCalc[1]])
            self.fenAnimalsCalc = self.modelObject.updataFenData(self.popAnimals,self.Sanimal)
            self.fenAnimalsMean_t.extend([self.fenAnimalsCalc[0]])
            self.fenAnimalsSD_t.extend([self.fenAnimalsCalc[1]])
            #apenas barra de progresso...
            percent = float(t+1) / self.time
            hashes = '||' * int(round(percent * 50))
            spaces = '-' * (50 - len(hashes))
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()

        #outputs
        self.outputPlantsPop = pd.DataFrame(self.abundancePlants_t)
        self.outputAnimalPop = pd.DataFrame(self.abundanceAnimals_t)
        self.outputPlantsFenMean = pd.DataFrame(self.fenPlantsMean_t)
        self.outputAnimalFenMean = pd.DataFrame(self.fenAnimalsMean_t)
        self.outputPlantsFenSD = pd.DataFrame(self.fenPlantsSD_t)
        self.outputAnimalFenSD = pd.DataFrame(self.fenAnimalsSD_t)
        self.outputInteractionMatrix  = self.interactionMatrix

