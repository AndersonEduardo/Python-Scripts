#FONTE: https://github.com/hnasr/python_playground/blob/master/mysqldemopython/db.py

#python3.7 -m pip install mysql-connector-python
import mysql.connector
import pandas as pd

#conectando a db
con =  mysql.connector.connect(
    host = 'anderson-G7-7588',
    user = 'root',
    password = '123123',
    database = 'dbteste',
    port = 3306
)

#imprimindo status
print('Conecção com banco de dados MySQL estabelecida com sucesso!')

#inicializando cursor
cur = con.cursor()

# aqui vem a interacao com o banco de dados taraves das queries#

#exemplo: inserindo dados da tabela
cur.execute('INSERT INTO user (id, nome, email, senha, telefone, foto, role, ativo) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)', 
            ('Blodivaldo Parara', 'blodi@email.com', '123sd13d', '(823)023-23923', 'NULL', 'usuario comum', '1')) #query

#exemplo: query para ler dados da tabela
cur.execute('SELECT * FROM user') #query
output = cur.fetchall() #pegando resultados da query
outputDB = pd.DataFrame(output)

print(outputDB)

#exemplo: percentual de usuarios ativos
import numpy as np
pecActUsrs = (np.sum(outputDB.iloc[:,7]) / len(outputDB)) * 100

print( '\nAtividade média dos usuários: ' + str(pecActUsrs) + '%\n')

#incorporando de fato alteracoes no MySQL
#con.commit()

#finalizando cursor
cur.close()

#finalizando conexao
con.close()
