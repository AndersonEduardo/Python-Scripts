import os 
os.chdir('/home/anderson/Documentos/Projetos/Redes Mutualisticas e Coevolucao') #MTA ATENCAO AQUI: diretorio de trabalho!
import time

start_time = time.time()
mensagem = '||| Runing Nuismer Model |||'
print mensagem.center(100)
###########
###########

N = 500
Sanimal = 6
Splants = 6
offspring = 5
carringCapacity = 500
alphaVector = [0.5]#[0.01,0.5,0.9]
gammaVector = [0.5]#[0.01,0.5,0.9]
thetaAnimal = range(Sanimal) #[rd.randint(10+Sanimal,50+Sanimal) for i in range(Sanimal)]
thetaPlants = range(Splants) #[rd.randint(10+Splants,50+Splants) for i in range(Splants)]
timeLen = 40

for alpha in alphaVector:
    for gamma in gammaVector:
        mymodel = nuismerModel(N,Sanimal,Splants,offspring,carringCapacity,alpha,gamma,thetaAnimal,thetaPlants,timeLen) #paratriza o modelo
        mymodel.run() #roda
        #salvando arquivos
        pd.DataFrame(mymodel.outputInteractionMatrix).to_csv('intMat'+str(alpha)+str(gamma)+'.csv') #salva matriz de interacao como arquivo .csv
        # pd.DataFrame(mymodel.outputPlantsPop).to_csv('plaPop'+str(alpha)+str(gamma)+'.csv') #salva abundancia de plantas como arquivo .csv
        # pd.DataFrame(mymodel.outputAnimalPop).to_csv('aniPop'+str(alpha)+str(gamma)+'.csv') #salva abundancia de animais como arquivo .csv
        # pd.DataFrame(mymodel.outputAnimalFenMean).to_csv('aniFenMean'+str(alpha)+str(gamma)+'.csv') #salva fenotipo medio das sps animais como .csv
        # pd.DataFrame(mymodel.outputAnimalFenSD).to_csv('aniFenSD'+str(alpha)+str(gamma)+'.csv') #salva SD do fenotipo de animais como arquivo .csv
        # pd.DataFrame(mymodel.outputPlantsFenMean).to_csv('plaFenMean'+str(alpha)+str(gamma)+'.csv') #salva fenotipo medio das sps plantas como .csv
        # pd.DataFrame(mymodel.outputPlantsFenMean).to_csv('plaFenSD'+str(alpha)+str(gamma)+'.csv') #salva SD do fenotipo de plantas como arquivo .cs

print mymodel.outputInteractionMatrix        
pl.plot(mymodel.outputAnimalPop)
pl.plot(mymodel.outputPlantsPop)
#pl.plot(mymodel.outputAnimalFenMean)
#pl.plot(mymodel.outputPlantsFenMean)
pl.show()

###########
###########
print '\nTime: %s minutes\n'  % ((time.time()-start_time)/60)

# import sys
# bar_length=50
# end_val = 500
# for i in xrange(0, end_val):
#         time.sleep(0.01)
#         percent = float(i) / end_val
#         hashes = '#' * int(round(percent * bar_length))
#         spaces = ' ' * (bar_length - len(hashes))
#         sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
#         sys.stdout.flush()

# print "\nFim!!\n"
