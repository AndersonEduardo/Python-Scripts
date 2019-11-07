import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

dados = pd.DataFrame({'colA':['a', 'a', 'b', 'b', 'c', 'c','d','e'],
                      'colB':['c', 'b', 'a', 'c', 'a', 'd','e','d']})
dados.sample(100, replace=True)

g = nx.from_pandas_edgelist(dados, 'colA', 'colB')
nx.draw(g)
plt.show()

print(nx.info(g))
print(nx.density(g))
print(nx.shortest_path(g, 'a', 'e'))
print(nx.diameter(g))
print(nx.connected_components(g))
