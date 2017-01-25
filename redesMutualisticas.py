import numpy as np
import random as rd
import matplotlib.pyplot as pl
import pandas as pd

class organisms:
    def __init__(self,group,sp,fen):
        self.group = group
        self.sp = sp #definindo a especie do organismo
        self.fen = fen #definindo seu genotipo
        self.statusLife = 1 #definindo se esta vivo
        self.age = 0

class environment:
    def __init__(self,N,Sanimal,Splants,alpha,gamma,theta):
        self.population = [] #array de populacoes
        self.abundancePlants = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        self.abundanceAnimal = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        self.numInd = N #definindo o numero de individuos no ambiente
        self.numSpAn = Sanimal #definindo o numero de especies animais
        self.numSpPlan = Splants #definindo o numero de especies plantas
        self.alpha = alpha
        self.gamma = gamma
        self.theta = theta

    def criatePop(self):
        for group in ['A','P']: #loop sobre grupos animal e planta
            if group == 'A':
                for i in range(self.numSpAn): #loop sobre numero de especies
                    for j in range(self.numInd): #loop sobre o numero de individuos
                        self.fenInitial = self.theta + np.random.uniform()
                        self.ind = organisms(group,i,self.fenInitial) #criando um organismo animal
                        self.population.append(self.ind) #adicionando o novo organismo no final do array de organismos
            else:
                for i in range(self.numSpPlan): #loop sobre numero de especies
                    for j in range(self.numInd): #loop sobre o numero de individuos
                        self.fenInitial = self.theta + np.random.uniform()
                        self.ind = organisms(group,i,self.fenInitial) #criando um organismo planta
                        self.population.append(self.ind) #adicionando o novo organismo no final do array de organismos

    def reproduction(self): #reproducao assexuada (depende apenas da interacao)
        for i in range(len(self.population)): #loop sobre o numero de organismos
            self.indGroup = self.population[i].group #registrando o grupo do organismo atual (se animal ou planta)
            self.intParGroup = [x for x in self.population if x.group != self.indGroup] #agrupando organismos do outro grupo para interacao
            if len(self.intParGroup) == 0:
                print "\n Colpased network: only " + self.indGroup + "remained in the system. :( \n"
                break
            
            self.intPar = rd.randint(0,len(self.intParGroup)-1) #sorteando o parceiro de interacao
            self.Za = filter(lambda x: x.group=='A',[self.population[i],self.intParGroup[self.intPar]]) #definindo Za
            self.Zp = filter(lambda x: x.group=='P',[self.population[i],self.intParGroup[self.intPar]]) #definindo Za
            
            self.indIntProb = self.interaction(self.Za[0].fen,self.Zp[0].fen,self.alpha) #obtendo valor da funcao para prob. de interacao

            if self.indIntProb > np.random.uniform():
                self.indFitness = self.fitness(self.population[i].fen,self.gamma,self.theta)

                if self.indFitness > np.random.uniform():
                    self.indSp = self.population[i].sp
                    self.indFen = self.population[i].fen
                    self.ind = organisms(self.indGroup,self.indSp,self.indFen+np.random.normal(0,1)) #criando um novo organismo...
                    self.population.append(self.ind) #adicionando novo ind a populacao.
                    #self.nind = len([x for x in self.populacao if x.group != self.indGroup]) #registrando o tamanho da populacao

    def interaction(self,Za,Zp,alpha): #funcao para prob. de interacao (Nuismer et al. 201..)
        self.fZaZp = 1.0 / ( 1.0+np.exp(-alpha*(Za-Zp)) )
        return self.fZaZp

    def fitness(self,Zy,gamma,theta): #funcao para o fitness de cada organismo (Nuismer et al. 201..)
        self.wZy = np.exp(-gamma*(Zy-theta)**2)
        return self.wZy

    def death(self):
        for i in range(len(self.population)): #loop sobre cada organismo
            if self.population[i].age == 1:
                self.population[i].statusLife = 0
        self.population = [x for x in self.population if x.statusLife == 1] #contando e regitrando os organismos vivos na populacao
    
    def updatePop(self):
#        self.population = [x for x in self.population if x.statusLife == 1] #contando e regitrando os organismos vivos na populacao
        for group in ['A','P']: #loop sobre grupos animal e planta
            if group == 'A':
                for i in range(self.numSpAn): #loop sobre cada especie animal
                    self.contagem = len([x for x in self.population if (x.group == group) and (x.sp == i)]) #contando quantos existem
                    self.abundanceAnimal.append(self.contagem) #registrando na variavel 'abundanciaAnimal'
            else:
                for i in range(self.numSpPlan): #loop sobre cada especie de planta
                    self.contagem = len([x for x in self.population if (x.group == group) and (x.sp == i)]) #contando quantas existem
                    self.abundancePlants.append(self.contagem) #registrando na variavel 'abundanciaPlants'
        for i in range(len(self.population)):
            self.population[i].age += 1 #aumentando em 1 unidade a idade
        #animal abundances data
        self.abundanceAnimalArray = np.array(self.abundanceAnimal) #transformando em 'array' (para o 'split')
        self.abundanceAnimalSplit = np.split(self.abundanceAnimalArray,len(self.abundanceAnimal)/(self.numSpAn)) #dividindo o array
        self.abundanceDataAnimal = pd.DataFrame(self.abundanceAnimalSplit) #transformando em 'array' em 'dataframe'
        #plants abundances data
        self.abundancePlantsArray = np.array(self.abundancePlants) #transformando em 'array' (para o 'split')
        self.abundancePlantsSplit = np.split(self.abundancePlantsArray,len(self.abundancePlants)/(self.numSpPlan)) #dividindo o array
        self.abundanceDataPlants = pd.DataFrame(self.abundancePlantsSplit) #transformando em 'array' em 'dataframe'

class nuismerModel:
    def __init__(self,N,Sanimal,Splants,alpha,gamma,theta,time):
        self.N = N
        self.Sanimal = Sanimal
        self.Splants = Splants
        self.alpha = alpha
        self.gamma = gamma
        self.theta = theta
        self.time = time
        self.setup = environment(self.N,self.Sanimal,self.Splants,self.alpha,self.gamma,self.theta)
        self.setup.criatePop()
        self.setup.updatePop()
            
    def run(self):
        for i in range(self.time):
            self.setup.reproduction()
            self.setup.death()
            self.setup.updatePop()
        self.outputAnimal = self.setup.abundanceDataAnimal
        self.outputPlants = self.setup.abundanceDataPlants
