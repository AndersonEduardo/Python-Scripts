import numpy as np
import random as rd
import matplotlib.pyplot as pl


class organisms:
    def __init__(self,group,sp,fen):
        self.group = group
        self.sp = sp #definindo a especie do organismo
        self.fen = fen #definindo seu genotipo
        self.statusLife = 1 #definindo se esta vivo
        self.age = 0

class environment:
    def __init__(self,N,G,S,alpha,gamma,theta):
        self.population = [] #array de populacoes
        self.abundancePlants = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        self.abundanceAnimal = [] #variavel para armazenar info dos tamanhos populacionais em cada passo de tempo
        self.numInd = N #definindo o numero de individuos no ambiente
        self.numSp = S #definindo o numero de especies no ambiente
        self.alpha = alpha
        self.gamma = gamma
        self.theta = theta

    def criatePop(self):
        for group in ['A','P']: #loop sobre grupos animal e planta
            for i in range(self.numSp): #loop sobre numero de especies
                for j in range(self.numInd): #loop sobre o numero de individuos
                    self.fenInitial = self.theta + np.random.uniform()
                    self.ind = organisms(group,i,self.fenInitial) #criando um organismo
                    self.population.append(self.ind) #adicionando o novo organismo no final do array de organismos

    def reproduz(self): ####AJUSTAR PARA REPRODUCAO SEXUADA
        for i in range(len(self.population)): #loop sobre o numero de organismos
            self.indGroup = self.population[i].group #verificando se o organismo atual e animal ou planta
            self.intParGroup = [x for x in self.populacao if x.group != self.indGroup] #agrupando grupo de organismos para interacao
            self.intPar = rd.randint(0,len(self.intParGroup)-1) #sorteando o parceiro de interacao
            self.Za = filter(lambda x: x.group=='A',[self.population[i],self.population[self.intPar]]) #definindo Za
            self.Zp = filter(lambda x: x.group=='P',[self.population[i],self.population[self.intPar]]) #definindo Za
            
            self.indIntProb = interaction(self.Za[0].fen,self.Zp[0].fen,self.alpha) #obtendo valor da funcao para prob. de interacao

            if self.indIntProb > np.random.uniform():
                self.indFitness = fitness(self.population[i].fen,self.theta)

                if self.indFitness > np.random.uniform():
                    self.indSp = self.population[i].sp
                    self.indFen = self.population[i].fen
                    self.ind = organisms(self.indGroup,self.indSp,self.indFen+np.random.normal(0,1)) #criando um novo organismo...
                    self.population.append(self.ind) #adicionando novo ind a populacao.
                    #self.nind = len([x for x in self.populacao if x.group != self.indGroup]) #registrando o tamanho da populacao

    def interaction(self,Za,Zp,alpha):
        self.fZaZp = 1.0 / ( 1.0+np.exp(-self.alpha*(self.Za-self.Zp)) )
        return self.fZaZp

    def fitness(self,Zy,gamma,theta):
        self.wZy = np.exp(-self.gamma*(self.Zy-self.theta)**2)
        return self.wZy

    def morre(self):
        for i in range(len(self.populacao)): #loop sobre cada organismo
            if self.populacao[i].age == 1:
                self.populacao[i].statusVida = 0
    
    def atualizaPop(self):
        self.populacao = [x for x in self.populacao if x.statusVida == 1] #contando e regitrando o numero de organismos vivos na populacao
        for group in ['A','P']: #loop sobre grupos animal e planta
            for i in range(self.numSp): #para cada especie...
                self.contagem = len([x for x in self.populacao if (x.group == group) and (x.Sp == i)]) #...conte quantos existem...
                if group == 'A':
                    self.abundanceAnimal.append(self.contagem) #...e registre na variavel 'abundancia'.
                else:
                    self.abundancePlants.append(self.contagem) #...e registre na variavel 'abundancia'.

            #####CCONTINUAR DAQUI:
            ##(ATENCAO: FALTA COLOCAR PARA ATULIZAR A IDADE DOS ORGNISMOS)
        self.abundanciaArray = np.array(self.abundancia) #transformando em 'array'
        self.abundanciaSplit = np.split(self.abundanciaArray,len(self.abundancia)/(self.numSp*self.numGen)) #dividindo o array
        self.abundanciaDados = pd.DataFrame(self.abundanciaSplit) #transformando em 'array' em 'dataframe'


