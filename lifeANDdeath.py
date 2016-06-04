##MODELO DE MORTE-VIDA COM GENOTIPOS E ORGANISMOS HAPLOIDES##
import numpy as np
import pandas as pd
import random as rd

class organismos:
    def __init__(self,s,g,p):
        self.Sp = s #definindo a especie do organismo
        self.Gen = g #definindo seu genotipo
        self.parasitado = 0  #definindo seu status parasitologico
        self.statusVida = 1 #definindo se esta vivo


class ambiente:
    def __init__(self,N,G,S):
        self.populacao = [] #array de populacoes
        self.abundancia = [] #variavel para armazenar os tamanhos populacionais em cada passo de tempo
        self.numInd = N #definindo o numero de individuos no ambiente
        self.numGen = G #definindo o numero de genotipos no ambiente
        self.numSp = S #definindo o numero de especies no ambiente
        #self.numPar = ?? #definindo o numero de parasitas no ambiente
        
    def criaPop(self):
        for i in range(self.numSp): #para cada especie...
            for j in range(self.numGen): #...e para cada um de seus genotipos...
                for k in range(self.numInd): #...crie 'numInd' organismos.
                    self.ind = organismos(i,j,0) #criando um organismo #############parasitado?################
                    self.populacao.append(self.ind) #adicionando o novo organismo no final do array de organismos

    def reproduz(self): ####AJUSTAR PARA REPRODUCAO SEXUADA
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            self.sucesso = rd.randint(0,1) #...jogue uma moeda...
            if self.sucesso >= 0: #...e se obtiver sucesso...
                self.parceiroReprodutivo = rd.randint(0,len(self.populacao)-1) #...sorteie o parceiro reprodutivo...
                self.genotipoDoParceiro = self.populacao[self.parceiroReprodutivo].Gen #..pegue o parceiro reprodutivo sorteado...
                self.quemsou = self.populacao[i].Sp #...veja qual a especie do organismo i...
                self.meuGenotipo = self.populacao[i].Gen #...veja qual e seu genotipo...
                self.ind = organismos(self.quemsou,rd.choice([self.meuGenotipo,self.genotipoDoParceiro]),0) #...crie um novo organismo...
                self.populacao.append(self.ind) #...e o adicione a populacao.
                self.nind = len(self.populacao)  #obtendo o tamanho da populacao

    def morre(self):
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if self.populacao[i].statusVida == 1:
                self.populacao[i].statusVida = 0
    
    def atualizaPop(self):
        self.populacao = [x for x in self.populacao if x.statusVida == 1] #contando e regitrando o numero de organismos vivos na populacao
        for i in range(self.numSp): #para cada especie...
            for j in range(self.numGen): #...e para cada um de seus genotipos...
                self.contagem = len([x for x in self.populacao if (x.Gen == j) and (x.Sp == i)]) #...conte quantos existem...
                self.abundancia.append(self.contagem) #...e registre na variavel 'abundancia'.

        self.abundanciaArray = np.array(self.abundancia) #transformando em 'array'
        self.abundanciaSplit = np.split(self.abundanciaArray,len(self.abundancia)/(self.numSp*self.numGen)) #dividindo o array
        self.abundanciaDados = pd.DataFrame(self.abundanciaSplit) #transformando em 'array' em 'dataframe'
                

class start:
    def __init__(self,n,g,s):
        self.Nind = n
        self.Ngen = g
        self.Nsp = s
        self.tempo = 13
        self.minhaPop = ambiente(self.Nind,self.Ngen,self.Nsp)
        self.minhaPop.criaPop()
        self.minhaPop.atualizaPop()
            
    def roda(self):
        for i in range(self.tempo):
            self.minhaPop.morre()
            self.minhaPop.reproduz()
            self.minhaPop.atualizaPop()
        self.res = self.minhaPop.abundanciaDados
