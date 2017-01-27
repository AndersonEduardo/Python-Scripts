mymodel = nuismerModel(10,2,2,3,20,0.05,0.05,2,2)
mymodel.run()

pl.plot(mymodel.outputAnimalPop)
#pl.plot(mymodel.outputPlantsPop)
#pl.plot(mymodel.outputAnimalFen)
pl.show()
