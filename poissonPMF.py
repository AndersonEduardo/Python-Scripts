def poissonPMF(a, b):
    poissonPMF = []
    mu = a
    k = b
    for ki in range(k):
        poissonPMF.append( (np.exp(-mu)*mu**ki)*(math.factorial(ki))**-1 )
    return poissonPMF
