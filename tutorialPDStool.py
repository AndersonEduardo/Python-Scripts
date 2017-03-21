##tutorial obtido de: http://www.ni.gsu.edu/~rclewley/PyDSTool/Tutorial/Tutorial_linear.html##Acesso: 21/mar/2017

import PyDSTool as dst
import pylab as pl
import numpy as np

#sistema de equacoes do modelo
dNdt = 'a*N*(1-N/k) - b*N*P'
dPdt = 'b*N*P - c*P'

#variaveis
vardict = {'N': dNdt,
           'P': dPdt}

#condicoes iniciais
icdict = {'N': 20,
          'P': 10}

#parametros
pardict = {'a': 1,
           'k': 50,
           'b': 0.1,
           'c': 0.8}

#argumentos para PDStools
DSargs = dst.args()                   # create an empty object instance of the args class, call it DSargs
DSargs.name = 'Lotka_Volterra'  # name our model
DSargs.ics = icdict               # assign the icdict to the ics attribute
DSargs.pars = pardict             # assign the pardict to the pars attribute
DSargs.tdomain = [0, 100]            # declare how long we expect to integrate for -- Ands: ou seja, o range de tempo
DSargs.varspecs = vardict         # assign the vardict dictionary to the 'varspecs' attribute of DSargs

#usando tudo para montar um objeto para o PDStool trabalhar
DS = dst.Generator.Vode_ODEsystem(DSargs)

# #integrando o modelo e plotando
traj = DS.compute('Lotka_Volterra')
pointSet = traj.sample()
#
# pl.plot(pts['t'],pointSet['N'],label='N')
# pl.plot(pts['t'],pointSet['P'],label='P')
# pl.legend()
# pl.xlabel('Time')
# pl.show()

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

#Analise de bifurcacao
#DS.set(pars = {'b': 0} )       # Lower bound of the control parameter 
DS.set(ics =  {'N': pointSet['N'][-1],
               'P': pointSet['P'][-1]} )       # Close to one of the steady states -- pointSet['N'][-1] foi definido acima

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
PCargs.verbosity    = 1
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
#PC['EQ1'].backward()
PC.display(['c','N'], stability=True, figure=3)        # stable and unstable branches as solid and dashed curves, resp.
#pl.ylim(-10,10)
pl.show()

PCargs.name = 'EQ2'
PCargs.type = 'LP-C'
PCargs.initpoint = 'EQ1:BP1'
PCargs.freepars = ['c','b']
PCargs.MaxNumPoints = 200                      # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1E-1
PCargs.MinStepSize  = 1E-5
PCargs.StepSize     = 2E-2
PCargs.LocBifPoints = 'CP'                     # detect limit points / saddle-node bifurcations
PCargs.verbosity    = 1
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ2'].forward()
PC['EQ2'].backward()

# Plot bifurcation diagram
PC.display(('b','c'), stability=True, figure=4)
pl.show()
