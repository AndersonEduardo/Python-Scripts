# coding: utf-8

# Studying python `yield` for algorithm performance.
# Author: Anderson A. Eduardo
# Date: 05/jan/2020


def func1(p):
    '''
        F1: function which do not employ yield in the generation of parameters grid.
    '''
    output = []
    for par in zip(p):
        prod = 1
        for beta in par[0]:
            prod *= beta
        output.append(prod)
    return output


def func2(par):
    '''
        F2: function which employ yield in the generation of parameters grid.
    '''
    output = 1
    for beta in par:
        output *= beta
    return output


def generate_parms(m,n):
    '''
        Helper function for the emulation of parameters values for an experiment.
    '''
    output = []
    for _ in range(m):
        output.append(list(range(1,n+1)))
    return output


def generate_grid(arr): 
    '''
        Generator of parameters grid (i.e. every possible combination of parameters values).
        Modifyied from: Mohit Kumar
        URL: https://www.geeksforgeeks.org/combinations-from-n-arrays-picking-one-element-from-each-array/
    '''
      
    # number of arrays 
    n = len(arr) 
  
    # to keep track of next element  
    # in each of the n arrays 
    indices = [0 for i in range(n)] 
  
    while (1): 
  
        # prcurrent combination 
        output = []
        for i in range(n): 
            #print(arr[i][indices[i]]), end = " ") 
            output.append( arr[i][indices[i]] )
        #print()
        yield output
  
        # find the rightmost array that has more 
        # elements left after the current element 
        # in that array 
        next = n - 1
        while (next >= 0 and 
              (indices[next] + 1 >= len(arr[next]))): 
            next-=1
  
        # no such array is found so no more 
        # combinations left 
        if (next < 0): 
            return
  
        # if found move to next element in that 
        # array 
        indices[next] += 1
  
        # for all arrays to the right of this 
        # array current index again points to 
        # first element 
        for i in range(next + 1, n): 
            indices[i] = 0


def bench(fun, yield_=None, gridgen=None, rangegen=None, parms=None):
    '''
        Function for time measurement.
    '''
    if  yield_:
        start = time.time()
        param_values = rangegen(parms[0], parms[1])
        output = [fun(x) for x in gridgen(param_values)]
        end = time.time()
        timelapse = end - start
        return timelapse
    else:
        start = time.time()
        param_values = rangegen(parms[0], parms[1])
        grid = [x for x in gridgen(param_values)]
        output = fun(grid)
        end = time.time()
        timelapse = end - start
        return timelapse


def generate_comparisons(bench_pars, vars=None, instances=None):
    '''
        Compares the performance of cuncurrent functions, employing the `bench` function.
    '''
    output = {
        'n_vars':vars,
        'n_instances':instances,
        'yield_time':[],
        'nonyield_time':[],
        'yield_is_better':[],
        'yield_over_nonyield':[]
    }
    for n_vars in vars:
        for n_inst in instances:
            
            tf1 = bench(fun = bench_pars['nonyield'].get('fun'), 
                        yield_= bench_pars['nonyield'].get('yield_'), 
                        gridgen = bench_pars['nonyield'].get('gridgen'), 
                        rangegen = bench_pars['nonyield'].get('rangegen'), 
                        parms = (n_vars, n_inst))
            
            tf2 = bench(fun = bench_pars['yield'].get('fun'), 
                        yield_= bench_pars['yield'].get('yield_'), 
                        gridgen = bench_pars['yield'].get('gridgen'), 
                        rangegen = bench_pars['yield'].get('rangegen'), 
                        parms = (n_vars, n_inst))

            # tf1 = bench(fun=func1, yield_= True, gridgen=generate_grid, rangegen=generate_parms, parms=(n_vars, n_inst))
            # tf2 = bench(fun=func2, yield_= True, gridgen=generate_grid, rangegen=generate_parms, parms=(n_vars, n_inst))

            output['yield_is_better'].append(tf2 > tf1)
            output['nonyield_time'].append(tf1)
            output['yield_time'].append(tf2)
            output['yield_over_nonyield'].append(tf2/tf1)
    
    return output


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    import time

    replicates = 4
    counter = 0

    while counter < replicates:
        
        bench_pars = {
            'nonyield':{
                'fun':func1, 'yield_': False, 'gridgen':generate_grid, 'rangegen':generate_parms
            },
            'yield':{
                'fun':func2, 'yield_': True, 'gridgen':generate_grid, 'rangegen':generate_parms
                } 
        }

        test =  generate_comparisons(bench_pars=bench_pars, vars=[1, 5, 10], instances=[5])

        plt.plot(test['n_vars'], test['yield_time'], label='yield', c='blue')
        plt.plot(test['n_vars'], test['nonyield_time'], label='non-yield', c='orange')
        
        counter +=1

    plt.legend(['yield', 'non-yield'])
    plt.show()