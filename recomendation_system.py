## Exemplo de sistema de recomendacao usando embidings e Keras e em Python 3.7 ##
## FONTE: https://github.com/TannerGilbert/Tutorials/blob/master/Recommendation%20System/Recommendation%20System.ipynb ##

# libraries
from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE

# Preparando dados #

# dataset path
#pathToDataset = '/home/anderson/Downloads/ml-20m'
pathToDataset = '/home/anderson/Downloads/ratings.csv'

# importando o arquivo dados
dataset = pd.read_csv(pathToDataset)
dataset.head()

# separando dados para treino e teste do modelo
train, test = train_test_split(dataset, test_size=0.2, random_state=42)

# Construindo rede neural #

# dados do numero de usuarios e numero de livros
n_users = len(dataset.user_id.unique())
n_books = len(dataset.book_id.unique())

# criando embidings dos livros
book_input = Input(shape=[1], name="Book-Input")
book_embedding = Embedding(n_books+1, 5, name="Book-Embedding")(book_input) #gerou warning de deprecated
book_vec = Flatten(name="Flatten-Books")(book_embedding)

# criando embidings dos usuarios
user_input = Input(shape=[1], name="User-Input")
user_embedding = Embedding(n_users+1, 10, name="User-Embedding")(user_input)
user_vec = Flatten(name="Flatten-Users")(user_embedding)

## PARA UMA ABORDAGEM MAIS SIMPLES, USAR DOT PRODUCT ##
## combinando embidings usando produto dot
#prod = Dot(name="Dot-Product", axes=1)([book_vec, user_vec])

## PARA UMA ABORDAGEM MAIS PODEROSA, USAR REDE NEURAL PROPRIAMENTE DITA
# concatenar features
conc = Concatenate()([book_vec, user_vec])

# adcionando camadas densamente conectadas (fully-connected-layers)
fc1 = Dense(128, activation='relu')(conc)
fc2 = Dense(32, activation='relu')(fc1)

# camada de output
out = Dense(1)(fc2)

# criando e compilando modelo
model = Model([user_input, book_input], out)
model.compile('adam', 'mean_squared_error')

# Training the model #

# treinando modelo, salvando na maquina do usuario e visualizado seu desenpenho
history = model.fit([train.user_id, train.book_id], train.rating, epochs=5, verbose=1)
model.save('recomendation_model.h5')

## caso queira apenas abrir um modelo ja treiando
#from keras.models import load_model
#model = load_model('recomendation_model.h5')

plt.plot(history.history['loss'])
plt.xlabel("Epochs")
plt.ylabel("Training Error")
plt.show()

model.evaluate([test.user_id, test.book_id], test.rating)

# Fazendo as recomensacoes #

# criando dataset para fazer recommendacoes para UM usuario (PRIMEIRO USUARIO dos nossos dados, nesse exemplo)
book_data = np.array(list(set(dataset.book_id))) #id dos livros
user = np.array([1 for i in range(len(book_data))]) #vetor para ser preenchido, do tamanho do vetor de livros

# fazendo as predicoes
predictions = model.predict([user, book_data])
predictions = np.array([a[0] for a in predictions])
recommended_book_ids = (-predictions).argsort()

# visualizando predicaoes
print(recommended_book_ids)
print(predictions[recommended_book_ids])

books = pd.read_csv('/home/anderson/Downloads/books.csv')
books.head()
print(books[books['book_id'].isin(recommended_book_ids)][:10]) #visualizando as 10 primeiras recomendacoes

# EXTRA: Visualizando embeddings #

# modulos necessarios
from sklearn.decomposition import PCA
import seaborn as sns

# extraindo embeddings
book_em = model.get_layer('Book-Embedding')
book_em_weights = book_em.get_weights()[0]

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(book_em_weights)

# gerando grafico
sns.scatterplot(x=pca_result[:,0], y=pca_result[:,1])