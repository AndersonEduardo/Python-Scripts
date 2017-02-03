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
    def __init__(self,alpha,gamma,thetaAnimal,thetaPlants,carringCapacity):
        self.alpha = alpha
        self.gamma = gamma
        self.thetaAnimal = thetaAnimal
        self.thetaPlants = thetaPlants
        self.carringCapacity = carringCapacity

    def criatePop(self,group,N,sp,offs):
        self.group = group
        self.numInd = N
        self.numSp = sp
        self.offspring = offs
        self.popNew = []
        if self.group == 'A':
            self.theta = self.thetaAnimal
        else:
            self.theta = self.thetaPlants
        for i in range(self.numSp): #loop sobre numero de especies
            self.sp_i = []
            for j in range(self.numInd): #loop sobre o numero de individuos
                self.sp_i.append(organisms(self.group,i,abs(self.theta[i] + np.random.uniform(-1,1)),self.offspring,0))
            self.popNew.append(self.sp_i) #add o novo organismo no final do array de organismos
        return self.popNew

    def reproduction(self,popAni,popPlan,nSp,thetaAni,thetaPla,eta,intMat): #reproducao assexuada (depende apenas da interacao)
        self.animalsPop = popAni
        self.plantsPop = popPlan
        self.numSp = nSp
        self.thetaAnimal = thetaAni
        self.thetaPlants = thetaPla
        self.eta = eta
        self.interactionMatrix = intMat
        if len(np.concatenate(self.plantsPop)) == 0:
            print "\n !!!The network collapsed!!! \n" 
        for i in range(self.numSp):
            for j in range(len(self.animalsPop[i])):
                if (self.animalsPop[i][j].age > 0):
                    self.visits = 0 #contador de visitas
                    for k in range(self.eta):
                        self.spPlan = rd.randint(0,len(self.plantsPop)-1)
                        self.indPlan = rd.randint(0,len(self.plantsPop[self.spPlan])-1)
                        self.intPlan = self.plantsPop[self.spPlan][self.indPlan] #planta (individuo) visitada pelo organismo animal atual
                        #obtendo valor da funcao para prob. de interacao
                        self.Za = self.animalsPop[i][j].fen
                        self.Zp = self.intPlan.fen
                        self.indIntProb = self.interaction(self.Za,self.Zp,self.alpha)
                        if self.indIntProb > np.random.uniform():
                            self.interactionMatrix[self.animalsPop[i][j].sp][self.intPlan.sp] += 1 #atualizando a matriz de interacao
                            self.visits += 1
                            #fitness da planta
                            self.indPlaFitness = self.fitness(self.intPlan.fen,self.gamma,self.thetaPlants[self.spPlan])
                            #reproducao plantas
                            if self.indPlaFitness > np.random.uniform():
                                for i_Offsp in range(self.intPlan.offspring): #add prole recursivamente para haver variabilidade em Fen.
                                    self.plantsPop[self.spPlan].extend([organisms('P',self.intPlan.sp,abs(np.random.normal(self.intPlan.fen)),self.intPlan.offspring,0)]) #adicionando novos inds na populacao.
                    if self.visits > 0:
                        self.indAniFitness = self.fitness(self.animalsPop[i][j].fen,self.gamma,self.thetaAnimal[i])
                        #reproducao animal
                        if self.indAniFitness > np.random.uniform():
                            for i_Offsp in range(self.animalsPop[i][j].offspring): #add prole recursivamente para haver variabilidade em Fen.
                                self.animalsPop[i].extend([organisms('A',self.animalsPop[i][j].sp,abs(np.random.normal(self.animalsPop[i][j].fen)),self.animalsPop[i][j].offspring,0)]) #adicionando novos inds na populacao.
        return self.animalsPop,self.plantsPop, self.interactionMatrix    

    def carringCapacityFunction(self,pop,nSp,k):
        self.pop = pop
        self.numSp = nSp
        self.carringCapacity = k
        self.updatedPop = []
        self.totalPop = np.concatenate(self.pop)
        for i in range(self.numSp):
            self.updatedPop.append(self.pop[i][:self.carringCapacity])
        return self.updatedPop
                
    def interaction(self,Za,Zp,alpha): #funcao para prob. de interacao (Nuismer et al. 201..)
        self.fZaZp = (1.0) / ( 1.0+np.exp((-1.0)*alpha*(Za-Zp)) )
        return self.fZaZp

    def fitness(self,Zy,gamma,theta): #funcao para o fitness de cada organismo (Nuismer et al. 201..)
        self.wZy = np.exp((-1.0)*gamma*((Zy-theta)**2))
        return self.wZy

    def updateAge(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        for i in range(self.numSp):
            for orgnsm in self.pop[i]:
                orgnsm.age+=1
        return self.pop 

    def death(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        self.updatedPop = []
        for i in range(self.numSp):
            for orgnsm in self.pop[i]:
                if orgnsm.age >=1:
                    orgnsm.statusLife = 0
            self.updatedPop.append([x for x in self.pop[i] if x.statusLife == 1])
        return self.updatedPop
    
    def updateAbundancesData(self,pop,nSp):
        self.pop = pop
        self.numSp = nSp
        self.abundance = []
        for i in range(self.numSp): #loop sobre cada especie animal
            self.abundance.append(len(self.pop[i])) #registrando na variavel 'abundanciaAnimal'
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
    def __init__(self,N,Sanimal,Splants,offs,carringCapacity,alpha,gamma,thetaAni,thetaPla,eta,time):        
        self.N = N
        self.Sanimal = Sanimal
        self.Splants = Splants
        self.offspring = offs
        self.carringCapacity = carringCapacity
        self.alpha = alpha
        self.gamma = gamma
        self.eta = eta
        self.thetaAnimal = thetaAni
        self.thetaPlants = thetaPla
        self.time = time
        self.modelObject = environment(self.alpha,self.gamma,self.thetaAnimal,self.thetaPlants,carringCapacity)
            
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
        self.popPlants = self.modelObject.criatePop('P',self.N,self.Splants,self.offspring)
        self.popAnimals = self.modelObject.criatePop('A',self.N,self.Sanimal,self.offspring)
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
            self.animalRep_t =  self.modelObject.reproduction(self.popAnimals,self.popPlants,self.Sanimal,self.thetaAnimal,self.thetaPlants,self.eta,self.interactionMatrix)
            self.popAnimals = self.animalRep_t[0]
            self.popPlants = self.animalRep_t[1]
            if t < int(0.8*self.time):
                self.interactionMatrix = np.zeros([self.Sanimal,self.Splants])
            else:
                self.interactionMatrix = self.animalRep_t[2]
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
            hashes = '#' * int(round(percent * 50))
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

