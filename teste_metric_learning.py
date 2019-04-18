import numpy as np
import matplotlib.pyplot as plt



def lossfunc(x, w):
    pa = x[0]
    pp = x[1]
    pn = x[2]

    #sigma = 0.01
    M = 5
    L_vec = np.array([])
    w_vec = [w[:]]

    for i in range(0,500):

        if i == 0:
            w11 = w[0] + np.random.normal(0, 0.1)
            w12 = w[1] + np.random.normal(0, 0.1)
            w21 = w[2] + np.random.normal(0, 0.1)
            w22 = w[3] + np.random.normal(0, 0.1)
            w31 = w[4] + np.random.normal(0, 0.1)
            w32 = w[5] + np.random.normal(0, 0.1)

            #dist_p = np.sqrt( ((w1*pa[0] - w1*pp[0])**2) + ((w2*pa[1] - w2*pp[1])**2) ) #dist pro ponto positivo
            #dist_n = np.sqrt( ((w1*pa[0] - w1*pn[0])**2) + ((w2*pa[1] - w2*pn[1])**2) ) #dist pro ponto negativo
            dist_p = abs(w11*pa[0] - w21*pp[0]) + abs(w12*pa[1] - w22*pp[1])
            dist_n = abs(w11*pa[0] - w31*pn[0]) + abs(w12*pa[1] - w32*pn[1])


            L = max(dist_p - dist_n + M, 0)

            L_vec = np.append(L_vec, L)
            w_vec.append( (w11, w12, w21, w22, w31, w32) )

        else:
            w11 = w_vec[-1][0] + np.random.normal(0, 0.1)
            w12 = w_vec[-1][1] + np.random.normal(0, 0.1)
            w21 = w_vec[-1][2] + np.random.normal(0, 0.1)
            w22 = w_vec[-1][3] + np.random.normal(0, 0.1)
            w31 = w_vec[-1][4] + np.random.normal(0, 0.1)
            w32 = w_vec[-1][5] + np.random.normal(0, 0.1)

            #dist_p = np.sqrt( ((w1*pa[0] - w1*pp[0])**2) + ((w2*pa[1] - w2*pp[1])**2) ) #dist pro ponto positivo
            #dist_n = np.sqrt( ((w1*pa[0] - w1*pn[0])**2) + ((w2*pa[1] - w2*pn[1])**2) ) #dist pro ponto negativo

            dist_p = abs(w11*pa[0] - w21*pp[0]) + abs(w12*pa[1] - w22*pp[1])
            dist_n = abs(w11*pa[0] - w31*pn[0]) + abs(w12*pa[1] - w32*pn[1])

            L_new = max(dist_p - dist_n + M, 0)

            if L_new < L_vec[-1]:
                L_vec = np.append(L_vec, L_new)
                w_vec.append( (w11, w12, w21, w22, w31, w32) )
    
    idx = np.argmin(L_vec)
    w_output = w_vec[idx]

    return w_output 


##pipeline##


dados = np.array([[2,5.4], 
                [3,6.1],
                [4.1,4.9],
                [4.1,5.5],
                [3.7,6.9],
                [4.9,5.9]])

labels = np.array(['A','A','A','B','B','B'])


w_output = np.zeros([6,2])

for i in range(0,3):

    for j in range(0,100):

        pa_idx = i
        pp_idx = np.random.choice(range(0,3))
        while pp_idx == pa_idx:
            pp_idx = np.random.choice(range(0,3))
        pn_idx = np.random.choice(range(3,6))

        pa = dados[pa_idx]
        pp = dados[pp_idx]
        pn = dados[pn_idx]

        if i == 0:
            w_zero = (1,1,1,1,1,1)
            dados_i = np.array([pa, pp, pn])
            x = lossfunc(dados_i, w_zero)
        else:
            dados_i = np.array([pa, pp, pn])
            x = lossfunc(dados_i, x)

        w_output[pa_idx] = x[0:2]
        w_output[pp_idx] = x[2:4]
        w_output[pn_idx] = x[4:]



# dados originais
plt.scatter(dados.T[0], dados.T[1], color=['red','red','red','blue', 'blue','blue'])
#plt.show()
plt.scatter(w_output.T[0] * dados.T[0], w_output.T[0] * dados.T[0], color=['orange','orange','orange','lightblue', 'lightblue','lightblue'])
plt.show()