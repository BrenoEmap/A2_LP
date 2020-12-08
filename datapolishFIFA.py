"""Módulo de refinamento da base de dados do jogo FIFA 19

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from connectdb import data_fifa
from re import sub
from decimal import Decimal

df = data_fifa        

# 1: Como ocorre a distribuição de jogadores atuando pela sua respectiva nacionalidade?
df['Nationality'].value_counts() #-> retorna a distribuição dos jogadores por nacionalidade

# 2: Sabe-se que o Overall de um time influencia na probabilidade de vitória,
# empate ou derrota. Com isso, qual é o somatório de Overall dos jogadores
# por time?
df2 = df.loc[:,['Overall','Club']].sort_values(by=['Club'])
setC = {club for club in df['Club']}
d2 = {}
for clube in setC:
    OverallTotal = 0
    Num_Jogadores = len(df2.loc[(df2['Club'] == clube)])
    OverallTotal = df2.loc[(df2['Club'] == clube)]['Overall'].sum()
    Overall_Medio = OverallTotal/Num_Jogadores
    d2.update({clube:Overall_Medio})
    #print(f"O overall médio do clube {clube} é: {Overall_Medio}")
df2 = pd.DataFrame(list(d2.items()),columns = ['Clube','Overall_Medio']).sort_values(by='Overall_Medio').drop([131])


# 3: Quantos jogadores possuem seu overall rating abaixo, acima e igual ao seu
# potencial esperado? E qual é o desvio padrão?
abaixo = df.loc[(df['Overall'] < df['Potential']), ['Overall','Potential']] #-> 12047
igual = df.loc[(df['Overall'] == df['Potential']), ['Overall','Potential']] #-> 6160
acima = df.loc[(df['Overall'] > df['Potential']), ['Overall','Potential']] #-> 0

if True:
    x = []
    soma_de_overall = df['Overall'].sum()
    quant_jogadores = len(df)
    overall_medio_total = soma_de_overall/quant_jogadores
        
    for valor in df['Overall']:
        x += [valor]
        
    for i in x:
       i = (i - overall_medio_total)**2

    soma = 0
    for i in x:
        soma = soma + i

    desv_pad = (soma/quant_jogadores)**0.5
    
print(f"Desvio padrão: {desv_pad}") #-> 8.13871607818636

total = len(acima) + len(abaixo) + len(igual)
prob_acima = len(acima)/total
prob_igual = len(igual)/total
prob_abaixo = len(abaixo)/total

y = np.array([len(abaixo), len(igual), len(acima)])
mylabels = [f"Abaixo {prob_abaixo}", f"Igual {prob_igual}", f"Acima {prob_acima}"]

plt.pie(y, labels = mylabels, shadow = True)
plt.show()

#4: Qual a média da idade dos jogadores? Quantos jogadores estão acima da média de idade?
np.mean(df['Age']) #-> 25.122205745043114
len(df.loc[(df['Age']>np.mean(df['Age'])), ['Name']]) #-> 8108

#5: Qual a média de idade por clubes?
df5 = df.loc[:,['Age', 'Club']].sort_values(by=['Club'])
setC = {club for club in df['Club']}
d5 = {}
for clube in setC:
    IdadeTotal = 0
    Num_Jogadores = len(df5.loc[(df5['Club'] == clube)])
    IdadeTotal = df5.loc[(df5['Club'] == clube)]['Age'].sum()
    Idade_Media = IdadeTotal/Num_Jogadores
    d5.update({clube:Idade_Media})
    #print(f"O overall médio do clube {clube} é: {Overall_Medio}")
df5 = pd.DataFrame(list(d5.items()),columns = ['Clube','Idade_Media']).sort_values(by='Idade_Media').drop([131])    

#6: Como ocorre a distribuição de jogadores canhotos e destros por posição?
df6 = df.loc[:,['Preferred_Foot','Position']].sort_values(by='Position').dropna()
d6 = dict.fromkeys(df6["Position"].values)
for position in d6.keys():
    data = df6.loc[df6["Position"] == position]["Preferred_Foot"]
    right = (data.value_counts())["Right"]
    left = (data.value_counts())["Left"]
    d6[position] = {"Right": right, "Left": left}
df6 = pd.DataFrame(d6).T
