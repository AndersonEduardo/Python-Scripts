import numpy as np
import random as rd
import matplotlib.pyplot as pl
import pandas as pd

class organisms(object):
    def __init__(self,group,sp,fen,offs,age):
        self.group = group
        self.sp = sp #definindo a especie do organismo
        self.fen = fen #definindo seu genotipo
        self.offspring = offs 
        self.statusLife = 1 #definindo se esta vivo
        self.age = age

class environment(object):
    def __init__(self,N,Sanimal,Splants,offs,alpha,gamma,theta,carringCapacity):
#        self.population = [] #array de populacoes
        self.abundancePlants = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        self.abundanceAnimal = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        self.plantsFenDataList = []
        self.animalFenDataList = []
        self.numInd = N #definindo o numero de individuos no ambiente
        self.numSpAn = Sanimal #definindo o numero de especies animais
        self.numSpPlan = Splants #definindo o numero de especies plantas
        self.offspring = offs 
        self.alpha = alpha
        self.gamma = gamma
        self.theta = theta
        self.carringCapacity = carringCapacity

    def criatePopAnimal(self):
        for i in range(self.numSpAn): #loop sobre numero de especies
            for j in range(self.numInd): #loop sobre o numero de individuos
                self.population.append(organisms('A',i,self.theta + np.random.uniform(),self.offspring,0)) #add o novo organismo no final do array de organismos

    def criatePopPlants(self):
        for i in range(self.numSpPlan): #loop sobre numero de especies
            for j in range(self.numInd): #loop sobre o numero de individuos
                self.population.append(organisms('P',i,self.theta + np.random.uniform(),self.offspring,0)) #add o novo organismo no final do array de organismos

    def animalReproduction(self,popAni,popPlan): #reproducao assexuada (depende apenas da interacao)
        self.animalsPop = popAni
        self.plantsPop = popPlan
        for i in range(len(self.animalsPop)):
            if (self.animalsPop[i].age > 0):
                if len(self.plantsPop) == 0:
                    print "\n !!!The network collapsed!!! \n"
                #obtendo valor da funcao para prob. de interacao
                self.Za = self.animalsPop[i].fen
                self.Zp = self.plantsPop[rd.randint(0,len(self.plantsPop)-1)].fen
                
                self.indIntProb = self.interaction(self.Za,self.Zp,self.alpha) 

                if self.indIntProb > np.random.uniform():
                    self.indFitness = self.fitness(self.animalsPop[i].fen,self.gamma,self.theta)

                    if self.indFitness > np.random.uniform():
                        for i_Offsp in range(self.animalsPop[i].offspring): #add prole recursivamente para haver variabilidade em Fen.
                            self.population.extend([organisms('A',self.animalsPop[i].sp,self.animalsPop[i].fen+np.random.normal(0,1),self.offspring,0)]) #adicionando novos inds na populacao.

    def plantsReproduction(self,popPlan,popAni): #reproducao assexuada (depende apenas da interacao)
        self.plantsPop = popPlan
        self.animalsPop = popAni
        for i in range(len(self.plantsPop)):
            if (self.plantsPop[i].age > 0):
                if len(self.animalsPop) == 0:
                    print "\n !!!The network collapsed!!! \n"
                #obtendo valor da funcao para prob. de interacao
                self.Za = self.animalsPop[rd.randint(0,len(self.animalsPop)-1)].fen
                self.Zp = self.plantsPop[i].fen

                self.indIntProb = self.interaction(self.Za,self.Zp,self.alpha) 

                if self.indIntProb > np.random.uniform():
                    self.indFitness = self.fitness(self.plantsPop[i].fen,self.gamma,self.theta)

                    if self.indFitness > np.random.uniform():
                        for i_Offsp in range(self.plantsPop[i].offspring): #add prole recursivamente para haver variabilidade em Fen.
                            self.population.extend([organisms('P',self.plantsPop[i].sp,self.plantsPop[i].fen+np.random.normal(0,1),self.offspring,0)]) #adicionando novos inds na populacao.

    def AnimalsCarringCapacity(self,popAni,k):
        self.animalsPop = popAni
        self.carringCapacity = k
        self.animalsPop = self.animalsPop[:self.carringCapacity]
        return self.animalsPop
        
        rd.shuffle(self.population)
        self.population = self.population[:self.carringCapacity]
        # if len([x for x in self.population if x.group == 'A']) > self.carringCapacity:
        #     self.difference = len([x for x in self.population if x.group == 'A']) - self.carringCapacity
        #     for i in range(self.difference):
        #         [x for x in self.population if (x.group == 'A') and (x.age == 0)][0].statusLife = 0
        # self.population = [x for x in self.population if x.statusLife == 1]
                
    def PlantsCarringCapacity(self):
        rd.shuffle(self.population)
        if len([x for x in self.population if x.group == 'P']) > self.carringCapacity:
            self.difference = len([x for x in self.population if x.group == 'P']) - self.carringCapacity
            for i in range(self.difference):
                print [x for x in self.population if (x.group == 'P') and (x.age == 0)][0].statusLife
                [x for x in self.population if (x.group == 'P') and (x.age == 0)][0].statusLife = 0
                print [x for x in self.population if (x.group == 'P') and (x.age == 0)][0].statusLife
            self.population = [x for x in self.population if x.statusLife == 1]

    def interaction(self,Za,Zp,alpha): #funcao para prob. de interacao (Nuismer et al. 201..)
        self.fZaZp = 1.0 / ( 1.0+np.exp(-alpha*(Za-Zp)) )
        return self.fZaZp

    def fitness(self,Zy,gamma,theta): #funcao para o fitness de cada organismo (Nuismer et al. 201..)
        self.wZy = np.exp(-gamma*(Zy-theta)**2)
        return self.wZy

    def updateAge(self):
        for orgnsm in self.population:
#            print orgnsm.age
            orgnsm.age+=1
#            print orgnsm.age

    def death(self):
        for orgnsm in self.population:
#            print len(self.population)
            if orgnsm.age >=1:
                orgnsm.statusLife = 0
 #           print len(self.population)
        self.population = [x for x in self.population if x.statusLife == 1]
    
    def updateAbundancesData(self):
#        self.population = [x for x in self.population if x.statusLife == 1] #contando e regitrando os organismos vivos na populacao
        for group in ['A','P']: #loop sobre grupos animal e planta
            if group == 'A':
                for i in range(self.numSpAn): #loop sobre cada especie animal
                    self.contagemAnimal = len([x for x in self.population if (x.group == group) and (x.sp == i)]) #contando quantos existem
                    self.abundanceAnimal.append(self.contagemAnimal) #registrando na variavel 'abundanciaAnimal'
            if group == 'P':
                for i in range(self.numSpPlan): #loop sobre cada especie de planta
                    self.contagemPlants = len([x for x in self.population if (x.group == group) and (x.sp == i)]) #contando quantas existem
                    self.abundancePlants.append(self.contagemPlants) #registrando na variavel 'abundanciaPlants'
        #animal abundances data
        self.abundanceAnimalArray = np.array(self.abundanceAnimal) #transformando em 'array' (para o 'split')
        self.abundanceAnimalSplit = np.split(self.abundanceAnimalArray,len(self.abundanceAnimal)/(self.numSpAn)) #dividindo o array
        self.abundanceDataAnimal = pd.DataFrame(self.abundanceAnimalSplit) #transformando em 'array' em 'dataframe'
        #plants abundances data
        self.abundancePlantsArray = np.array(self.abundancePlants) #transformando em 'array' (para o 'split')
        self.abundancePlantsSplit = np.split(self.abundancePlantsArray,len(self.abundancePlants)/(self.numSpPlan)) #dividindo o array
        self.abundanceDataPlants = pd.DataFrame(self.abundancePlantsSplit) #transformando em 'array' em 'dataframe'

    def updataFenData(self):
        #animals 
        self.animalsPop = [x for x in self.population if x.group == 'A']
        self.animalFenArray = np.array([x.fen for x in self.animalsPop])
        self.animalFenMean = np.mean(self.animalFenArray)
        self.animalFenSD = np.std(self.animalFenArray)
        self.animalFenDataList.append([self.animalFenMean,self.animalFenSD])
        self.animalFenDataArray = np.array(self.animalFenDataList)
        self.animalFenData = pd.DataFrame(self.animalFenDataArray)
        #plants
        self.plantsPop = [x for x in self.population if x.group == 'P']
        self.plantsFenArray = np.array([x.fen for x in self.plantsPop])
        self.plantsFenMean = np.mean(self.plantsFenArray)
        self.plantsFenSD = np.std(self.plantsFenArray)
        self.plantsFenDataList.append([self.plantsFenMean,self.plantsFenSD])
        self.plantsFenDataArray = np.array(self.plantsFenDataList)
        self.plantsFenData = pd.DataFrame(self.plantsFenDataArray)


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
        self.modelObject = environment(self.N,self.Sanimal,self.Splants,self.offspring,self.alpha,self.gamma,self.theta,carringCapacity)
#        self.modelObject.criatePop()
            
    def run(self):
        self.modelObject.updateAbundancesData()
        self.modelObject.updataFenData()
        self.popAnimals = modelObject.criatePopAnimal()
        self.popPlants = modelObject.criatePopPlants()
        for t in range(self.time):
            self.popPlants = self.modelObject.updateAge(self.popPlants)
            ##CONTINUAR DAQUI: veriricar todos os passos e métodos desta funcao (run()) - comecei a mudar coisas la em cima.
            self.modelObject.updateAge(self.popAnimals)
            self.modelObject.plantsReproduction(self.popPlants,self.popAnimals)
            self.modelObject.animalReproduction(self.popAnimals,self.popPlants)
            
            self.modelObject.death(self.popPlants)
            self.modelObject.death(self.popAnimals)
            self.modelObject.PlantsCarringCapacity(self.popPlants)
            self.modelObject.AnimalsCarringCapacity(self.popAnimals)
            self.modelObject.updateAbundancesData(self.popPlants)
            self.modelObject.updateAbundancesData(self.popAnimals)
            self.modelObject.updataFenData(popPlants)
            self.modelObject.updataFenData(popAnimals)
        self.outputAnimalPop = self.modelObject.abundanceDataAnimal
        self.outputPlantsPop = self.modelObject.abundanceDataPlants
        self.outputAnimalFen = self.modelObject.animalFenData
        self.outputPlantsFen = self.modelObject.plantsFenData
