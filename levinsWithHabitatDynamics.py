##tutorial obtido de: http://www.ni.gsu.edu/~rclewley/PyDSTool/Tutorial/Tutorial_linear.html##Acesso: 21/mar/2017

import PyDSTool as dst
import pylab as pl
import numpy as np
    

## LEVINS MODEL (base model) ##


#sistema de equacoes do modelo
dNdt = 'c*N*(1-N) - d*N'

#variaveis
vardict = {'N': dNdt}

#condicoes iniciais
icdict = {'N': 0.5}

#parametros
pardict = {'c': 0.9,
           'd': 0.1}

#argumentos para PDStools
DSargs = dst.args()                   # create an empty object instance of the args class, call it DSargs
DSargs.name = 'Levins'  # name our model
DSargs.ics = icdict               # assign the icdict to the ics attribute
DSargs.pars = pardict             # assign the pardict to the pars attribute
DSargs.tdomain = [0, 100]            # declare how long we expect to integrate for -- Ands: ou seja, o range de tempo
DSargs.varspecs = vardict         # assign the vardict dictionary to the 'varspecs' attribute of DSargs
DS = dst.Generator.Vode_ODEsystem(DSargs)
traj = DS.compute('Levins')
pointSet = traj.sample()

pl.matplotlib.rc('xtick', labelsize=20)
pl.matplotlib.rc('ytick', labelsize=20)
pl.plot(pointSet['t'], pointSet['N'], linewidth=3.0)
pl.xlabel('Tempo', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.ylim(0,1)
pl.show()


##Analise de bifurcacao


##parametro 'c'

#DS.set(pars = {'c': 0} )       # Lower bound of the control parameter 
DS.set(ics =  {'N': pointSet['N'][-1]})       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ1'
PCargs.type         = 'EP-C'
PCargs.freepars     = ['c']                    # control parameter(s) (it should be among those specified in DSargs.pars)
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 2
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].backward()

PC.display(['c','N'], stability=True, figure=3)        # stable and unstable branches as solid and dashed curves, resp.
pl.ylim(-0.2,1.1)
pl.xlim(-0.2,1.1)
pl.xlabel('c', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()

#continuação
PCargs.name         = 'EQ1-2'
PCargs.type         = 'EP-C'
PCargs.initpoint    = 'EQ1:BP1'
PCargs.freepars     = ['c']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ1-2'].forward()
PC['EQ1-2'].backward()

PC['EQ1'].display(['c','N'], stability=True, figure=1)
PC['EQ1-2'].display(['c','N'], stability=True, figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.1,1.1)
pl.xlabel('c', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()


##parametro 'd'


DS.set(ics =  {'N': pointSet['N'][-1] } )       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ2'
PCargs.type         = 'EP-C'
#PCargs.initpoint = 'EQ1:BP1'
PCargs.freepars = ['d']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1E-1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 1
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ2'].forward()
PC['EQ2'].backward()

# Plot bifurcation diagram
PC.display(['d','N'], stability=True, figure=1)        # stable and unstable branches as solid and dashed curves, resp.
pl.ylim(-0.2,1.1)
pl.xlim(-0.2,1.1)
pl.xlabel('d', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()


#continuação
PCargs.name         = 'EQ2-2'
PCargs.type         = 'EP-C'
PCargs.initpoint    = 'EQ2:BP1'
PCargs.freepars     = ['d']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ2-2'].forward()
PC['EQ2-2'].backward()

PC['EQ2'].display(['d','N'], stability=True, figure=1)
PC['EQ2-2'].display(['d','N'], stability=True, figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.1,1.1)
pl.xlabel('d')
pl.xlabel('d', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()


## MODELO 01: alpha != beta, com alpha e beta > 0 ##


#sistema de equacoes do modelo
dNdt = '- N*beta - alpha + beta + N*(1-N)*c - N*d'
#dMdt = ' M*(alpha-beta) + N*d - N*M*c'

#variaveis
vardict = {'N': dNdt}

#condicoes iniciais
icdict = {'N': 0.5}

#parametros
pardict = {'c': 0.9, 'd': 0.1, 'alpha': 0.1, 'beta': 0.1}

#argumentos para PDStools
DSargs = dst.args()                   # create an empty object instance of the args class, call it DSargs
DSargs.name = 'Levins01'  # name our model
DSargs.ics = icdict               # assign the icdict to the ics attribute
DSargs.pars = pardict             # assign the pardict to the pars attribute
DSargs.tdomain = [0, 100]            # declare how long we expect to integrate for -- Ands: ou seja, o range de tempo
DSargs.varspecs = vardict         # assign the vardict dictionary to the 'varspecs' attribute of DSargs

#usando tudo para montar um objeto para o PDStool trabalhar
DS = dst.Generator.Vode_ODEsystem(DSargs)

# #integrando o modelo e plotando
traj = DS.compute('Levins01')
pointSet = traj.sample()


##Analise de bifurcacao


##parametro 'alpha'


DS.set(ics =  {'N': pointSet['N'][-1]})       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ1'
PCargs.type         = 'EP-C'
PCargs.freepars     = ['alpha']                    # control parameter(s) (it should be among those specified in DSargs.pars)
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 2
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].backward()

PC.display(['alpha','N'], stability=True, figure=1)        # stable and unstable branches as solid and dashed curves, resp.
pl.ylim(-0.1,1.1)
pl.xlim(-0.1,0.6)
pl.xlabel('Alpha', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()

#continuação
PCargs.name         = 'EQ1-2'
PCargs.type         = 'EP-C'
PCargs.initpoint    = 'EQ1:LP1'
PCargs.freepars     = ['alpha']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ1-2'].forward()
PC['EQ1-2'].backward()

PC['EQ1'].display(['alpha','N'], stability=True, figure=1)
PC['EQ1-2'].display(['alpha','N'], stability=True, figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.1,1.1)
pl.xlabel('Alpha', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()


##parametro 'beta'


DS.set(ics =  {'N': pointSet['N'][-1]})       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ2'
PCargs.type         = 'EP-C'
PCargs.freepars = ['beta']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1E-1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 1
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ2'].forward()
PC['EQ2'].backward()

PC['EQ2'].display(['beta','N'], stability=True, figure=3)
pl.ylim(-0.1,1.1)
pl.xlim(-0.5,1.1)
pl.xlabel('Beta', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()

#continuação

PCargs.name         = 'EQ2-2'
PCargs.type         = 'EP-C'
PCargs.initpoint    = 'EQ2:LP1'
PCargs.freepars     = ['beta']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ2-2'].forward()
PC['EQ2-2'].backward()

PC['EQ2'].display(['beta','N'], stability=True, figure=1)
PC['EQ2-2'].display(['beta','N'], stability=True, figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.5,1.1)
pl.xlabel('Beta', fontsize=20)
pl.ylabel('N', fontsize=20)
pl.show()


#ALPHA x BETA  #obs: rodar EQ1 e esse na sequencia para que aqui funcione!


PCargs.name         = 'EQ3'
PCargs.type         = 'LP-C'
PCargs.initpoint    = 'EQ1:LP1'
PCargs.freepars     = ['alpha','beta']
PCargs.MaxNumPoints = 100                     # The following 3 parameters are set after trial-and-error
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ3'].forward()
PC['EQ3'].backward()

PC['EQ3'].display(['alpha','beta'], figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.1,1.1)
pl.xlabel('Alpha', fontsize=20)
pl.ylabel('Beta', fontsize=20)
pl.show()


#ALPHA x c  #obs: rodar EQ1 e esse na sequencia para que aqui funcione!


PCargs.name         = 'EQ4'
PCargs.type         = 'LP-C'
PCargs.initpoint    = 'EQ1:LP1'
PCargs.freepars     = ['alpha','c']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ4'].forward()
PC['EQ4'].backward()

PC['EQ4'].display(['alpha','c'], figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.1,1.1)
pl.xlabel('Alpha', fontsize=20)
pl.ylabel('c', fontsize=20)
pl.show()


#BETA x c  #obs: rodar EQ1 e esse na sequencia para que aqui funcione!


PCargs.name         = 'EQ5'
PCargs.type         = 'LP-C'
PCargs.initpoint    = 'EQ1:LP1'
PCargs.freepars     = ['beta','c']
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.LocBifPoints = 'all'
PC.newCurve(PCargs)
PC['EQ5'].forward()
PC['EQ5'].backward()

PC['EQ5'].display(['beta','c'], figure=1)
pl.ylim(-0.1,1.1)
pl.xlim(-0.05,1.1)
pl.xlabel('Beta', fontsize=20)
pl.ylabel('c', fontsize=20)
pl.show()


## MODELO 02: alpha == beta ##


#sistema de equacoes do modelo
dNdt = '- N*omega - omega + omega + N*(1-N)*c - N*d'
#dMdt = ' M*(alpha-beta) + N*d - N*M*c'

#variaveis
vardict = {'N': dNdt}

#condicoes iniciais
icdict = {'N': 0.5}

#parametros
pardict = {'c': 0.9, 'd': 0.1, 'omega': 0.1}

#argumentos para PDStools
DSargs = dst.args()                   # create an empty object instance of the args class, call it DSargs
DSargs.name = 'Levins02'  # name our model
DSargs.ics = icdict               # assign the icdict to the ics attribute
DSargs.pars = pardict             # assign the pardict to the pars attribute
DSargs.tdomain = [0, 100]            # declare how long we expect to integrate for -- Ands: ou seja, o range de tempo
DSargs.varspecs = vardict         # assign the vardict dictionary to the 'varspecs' attribute of DSargs

#usando tudo para montar um objeto para o PDStool trabalhar
DS = dst.Generator.Vode_ODEsystem(DSargs)

# #integrando o modelo e plotando
traj = DS.compute('Levins02')
pointSet = traj.sample()
#
pl.plot(pointSet['t'],pointSet['N'],label='N')
pl.legend()
pl.xlabel('Time')
pl.show()

# #variando as condicoes iniciais
# pl.clf()                                       # Clear the figure
# pl.hold(True)                                  # Sequences of plot commands will not clear the existing figure
# for i, N0 in enumerate(np.linspace(0,20,20)):
#     DS.set( ics = { 'N': N0 } )                # Initial condition
#     # Trajectories are called x0, x1, ...
#     # sample them on the fly to create Pointset tmp
#     trajIC = DS.compute('trajIC%i' %i).sample()    # or specify dt option to sample to sub-sample
#     pl.plot(trajIC['t'], trajIC['N'])
# pl.xlabel('time')
# pl.ylabel('N')
# pl.title(DS.name + ' multi ICs')
# pl.show()


##Analise de bifurcacao


##parametro 'omega'

#DS.set(pars = {'c': 0} )       # Lower bound of the control parameter 
DS.set(ics =  {'N': pointSet['N'][-1]})       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ1'
PCargs.type         = 'EP-C'
PCargs.freepars     = ['omega']                    # control parameter(s) (it should be among those specified in DSargs.pars)
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1E-1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 2
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].backward()
PC.display(['omega','N'], stability=True, figure=1)        # stable and unstable branches as solid and dashed curves, resp.
#pl.ylim(-10,10)
pl.show()


## MODELO 03: alpha = 0 e beta > 0 ##


#sistema de equacoes do modelo
dNdt = '- N*beta + beta + N*(1-N)*c - N*d'
#dMdt = ' M*(alpha-beta) + N*d - N*M*c'

#variaveis
vardict = {'N': dNdt}

#condicoes iniciais
icdict = {'N': 0.5}

#parametros
pardict = {'c': 0.9, 'd': 0.1, 'beta': 0.1}

#argumentos para PDStools
DSargs = dst.args()                   # create an empty object instance of the args class, call it DSargs
DSargs.name = 'Levins03'  # name our model
DSargs.ics = icdict               # assign the icdict to the ics attribute
DSargs.pars = pardict             # assign the pardict to the pars attribute
DSargs.tdomain = [0, 100]            # declare how long we expect to integrate for -- Ands: ou seja, o range de tempo
DSargs.varspecs = vardict         # assign the vardict dictionary to the 'varspecs' attribute of DSargs

#usando tudo para montar um objeto para o PDStool trabalhar
DS = dst.Generator.Vode_ODEsystem(DSargs)

# #integrando o modelo e plotando
traj = DS.compute('Levins03')
pointSet = traj.sample()
#
pl.plot(pointSet['t'],pointSet['N'],label='N')
pl.legend()
pl.xlabel('Time')
pl.show()

# #variando as condicoes iniciais
# pl.clf()                                       # Clear the figure
# pl.hold(True)                                  # Sequences of plot commands will not clear the existing figure
# for i, N0 in enumerate(np.linspace(0,20,20)):
#     DS.set( ics = { 'N': N0 } )                # Initial condition
#     # Trajectories are called x0, x1, ...
#     # sample them on the fly to create Pointset tmp
#     trajIC = DS.compute('trajIC%i' %i).sample()    # or specify dt option to sample to sub-sample
#     pl.plot(trajIC['t'], trajIC['N'])
# pl.xlabel('time')
# pl.ylabel('N')
# pl.title(DS.name + ' multi ICs')
# pl.show()


##Analise de bifurcacao


##parametro 'beta'

#DS.set(pars = {'c': 0} )       # Lower bound of the control parameter 
DS.set(ics =  {'N': pointSet['N'][-1]})       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ1'
PCargs.type         = 'EP-C'
PCargs.freepars     = ['beta']                    # control parameter(s) (it should be among those specified in DSargs.pars)
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1E-1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 2
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].backward()
PC.display(['beta','N'], stability=True, figure=1)        # stable and unstable branches as solid and dashed curves, resp.
pl.ylim(-0.5,1.5)
pl.xlim(0,2)
pl.show()


## MODELO 04: alpha > 0 e beta = 0 ##


#sistema de equacoes do modelo
dNdt = '- alpha + N*(1-N)*c - N*d'
#dMdt = ' M*(alpha-beta) + N*d - N*M*c'

#variaveis
vardict = {'N': dNdt}

#condicoes iniciais
icdict = {'N': 0.5}

#parametros
pardict = {'c': 0.9, 'd': 0.1, 'alpha': 0.1}

#argumentos para PDStools
DSargs = dst.args()                   # create an empty object instance of the args class, call it DSargs
DSargs.name = 'Levins04'  # name our model
DSargs.ics = icdict               # assign the icdict to the ics attribute
DSargs.pars = pardict             # assign the pardict to the pars attribute
DSargs.tdomain = [0, 100]            # declare how long we expect to integrate for -- Ands: ou seja, o range de tempo
DSargs.varspecs = vardict         # assign the vardict dictionary to the 'varspecs' attribute of DSargs

#usando tudo para montar um objeto para o PDStool trabalhar
DS = dst.Generator.Vode_ODEsystem(DSargs)

# #integrando o modelo e plotando
traj = DS.compute('Levins04')
pointSet = traj.sample()
#
pl.plot(pointSet['t'],pointSet['N'],label='N')
pl.legend()
pl.xlabel('Time')
pl.show()

# #variando as condicoes iniciais
# pl.clf()                                       # Clear the figure
# pl.hold(True)                                  # Sequences of plot commands will not clear the existing figure
# for i, N0 in enumerate(np.linspace(0,20,20)):
#     DS.set( ics = { 'N': N0 } )                # Initial condition
#     # Trajectories are called x0, x1, ...
#     # sample them on the fly to create Pointset tmp
#     trajIC = DS.compute('trajIC%i' %i).sample()    # or specify dt option to sample to sub-sample
#     pl.plot(trajIC['t'], trajIC['N'])
# pl.xlabel('time')
# pl.ylabel('N')
# pl.title(DS.name + ' multi ICs')
# pl.show()


##Analise de bifurcacao


##parametro 'alpha'

#DS.set(pars = {'c': 0} )       # Lower bound of the control parameter 
DS.set(ics =  {'N': pointSet['N'][-1]})       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

PC = dst.ContClass(DS)            # Set up continuation class

PCargs              = dst.args()     # 'EP-C' stands for Equilibrium Point Curve. The branch will be labeled 'EQ1'.
PCargs.name         = 'EQ1'
PCargs.type         = 'EP-C'
PCargs.freepars     = ['alpha']                    # control parameter(s) (it should be among those specified in DSargs.pars)
PCargs.MaxNumPoints = 100                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1E-1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'all'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 2
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].backward()
PC.display(['alpha','N'], stability=True, figure=1)        # stable and unstable branches as solid and dashed curves, resp.
pl.ylim(-0.5,1.5)
pl.xlim(0,2)
pl.show()
