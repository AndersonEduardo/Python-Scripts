mymodel = nuismerModel(30,3,3,2,300,0.1,0.1,2,50)
mymodel.run()

pl.plot(mymodel.outputPlantsFen)
#pl.plot(mymodel.outputAnimalFen)
pl.show()
