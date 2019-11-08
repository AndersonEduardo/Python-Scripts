#coding utf-8#

## AUTÔMATO CELULAR DE 1 DIMENSÃO
# Requerimentos:
# -Python 3.6 ou posterior
# -módulo numpy
# -módulo matplotlib
#
# Como rodar:
# -abra um terminal (e.g., prompt de comandos do Windows)
# -navegue até o diretório em que está este arquivo
# -execute: python3 cellular_automata_1d.py
# :-)


import numpy as np
from matplotlib import pyplot as plt


class Lattice:


    def __init__(self, Xdim, Ydim):
        self.lattice = np.zeros([Xdim, Ydim])
        self._w = len(self.lattice[0])
        self._h = len(self.lattice)
        self.startLattice()


    def startLattice(self):
        midleCell = int(self._w/2) + 1
        self.lattice[0][midleCell] = 1

        return print('\nSTATUS: Lattice criado com sucesso!')


class Simulator:


    def __init__(self, lat_obj):
        self.lattice = lat_obj.lattice
        self._w = lat_obj._w
        self._h = lat_obj._h

        print('STATUS: Simulador criado com sucesso!')


    def run(self):

        for t in range(1,self._h): #time
            for s in range(self._w): #space

                if s == 0:
                    if self.lattice[t-1][s] == 1 or self.lattice[t-1][s+1] == 1:
                        self.lattice[t][s] = 1
                    if self.lattice[t-1][s] == 1 and self.lattice[t-1][s+1] == 1:
                        self.lattice[t][s] = 0

                elif s == (self._w-1):
                    if self.lattice[t-1][s] == 1 or self.lattice[t-1][s-1] == 1:
                        self.lattice[t][s] = 1
                    if self.lattice[t-1][s] == 1 and self.lattice[t-1][s-1] == 1:
                        self.lattice[t][s] = 0

                elif s > 0 and s < (self._w-1):
                    if self.lattice[t-1][s] == 1 or self.lattice[t-1][s-1] == 1 or self.lattice[t-1][s+1] == 1:
                        self.lattice[t][s] = 1
                    if self.lattice[t-1][s] == 1 and self.lattice[t-1][s-1] == 1 and self.lattice[t-1][s+1] == 1:
                        self.lattice[t][s] = 0

                else:
                    self.lattice[t][s] = 0
        
        print('STATUS: Simulação finalizada com sucesso! \n')

        return self.lattice


if __name__ == "__main__":

    print('\nOlá! Vamos simular um autômato celular?\n')
    x = int(input('Digite o valor para a largura do autômato (i.e., eixo X): '))
    y = int(input('Digite o valor para a altura do autômato (i.e., eixo Y): '))
    print('\nAgora vamos lá!')

    lat = Lattice(x, y) #inicializando o lattice
    it = Simulator(lat) #inicializando o simulador
    
    it.run() #rodando a simulacao
    print('Rodando...\n')

    print('Prontinho! Observe esses padrões! Uau...\n')
    print("(Pressione a tecla 'q' para sair)\n")

    plt.imshow(it.lattice, cmap='binary') #construindo grafico do lattice apos simulacao
    plt.show() #exibindo grafico
