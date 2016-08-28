import pandas as pd
import numpy as np

#Create dataframe (that we will be importing)
raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
df

#Save dataframe as csv in the working director
df.to_csv('../data/example.csv')

#Load a csv
df = pd.read_csv('../data/example.csv')
df

#Load a csv with no headers
df = pd.read_csv('../data/example.csv', header=None)
df

#Load a csv while specifying column names
df = pd.read_csv('../data/example.csv', names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df

#Load a csv with setting the index column to UID
df = pd.read_csv('../data/example.csv', index_col='UID', names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df

#Load a csv while setting the index columns to First Name and Last Name
df = pd.read_csv('../data/example.csv', index_col=['First Name', 'Last Name'], names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df

#Load a csv while specifying "." as missing values
df = pd.read_csv('../data/example.csv', na_values=['.'])
pd.isnull(df)

#Load a csv while specifying "." and "NA" as missing values in the Last Name column and "." as missing values in Pre-Test Score colum
sentinels = {'Last Name': ['.', 'NA'], 'Pre-Test Score': ['.']}

df = pd.read_csv('../data/example.csv', na_values=sentinels)
df

#Load a csv while skipping the top 3 rows
df = pd.read_csv('../data/example.csv', na_values=sentinels, skiprows=3)
df

#Load a csv while interpreting "," in strings around numbers as thousands seperators
df = pd.read_csv('../data/example.csv', thousands=',')
df














