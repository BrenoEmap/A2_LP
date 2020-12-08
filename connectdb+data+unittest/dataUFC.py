"""Módulo de refinamento da base de dados do UFC

"""
import numpy as np
import pandas as pd
import seaborn 
import matplotlib as plt
import re
from connectdb import data_ufc

df = data_ufc

weight_values = df['weight_class'].value_counts()

weight_values = weight_values.drop(labels = ["Catch Weight", "Lightweight","Welterweight", "Middleweight", "Featherweight", "Bantamweight", "Light Heavyweight", "Heavyweight", "Flyweight"])  #Catch Weight não é uma classe de pesos oficial.

weights = {"Catch Weight": 0, "Lightweight": 0,"Welterweight": 0, "Middleweight": 0, "Featherweight": 0, "Bantamweight": 0, "Light Heavyweight": 0, "Heavyweight": 0, "Flyweight": 0, "Women's Strawweight": 0, "Women's Bantamweight": 0, "Women's Flyweight": 0, "Women's Featherweight": 0}

# Número de lutadores por categoria 

for key in weights.keys():
    data = df.loc[df["weight_class"] == key]
    names = data["R_fighter"]
    names = names.append(data["B_fighter"])
    weights[key] = len(names.value_counts())
    
# Como a luta terminou, por ano  
   
years = {2020: "", 2019: "", 2018: "", 2017: "", 2016: "", 2015: "", 2014: "", 2013: "", 2012: "", 2011: "", 2010: "" }
    
for key in years.keys():
    data = df[df['date'].str.contains(rf'^{key}')]["finish"].value_counts()
    decision = int(data["U-DEC"]) + int(data["S-DEC"]) + int(data["M-DEC"])
    submission = int(data["SUB"])
    knockout = int(data["KO/TKO"])
    total = decision + submission + knockout
    years[key] = {"DEC": round(decision/total, 2), "SUB": round(submission/total, 2), "KO/TKO": round(knockout/total, 2)}
    
# Top 10 geral Feminino e Masculino (mais vitórias)

data_M = df.loc[df["gender"] == "MALE"]
data_M_blue = data_M.loc[df["Winner"] == "Blue"]
data_M_red = data_M.loc[df["Winner"] == "Red"]
data_M_winners = data_M_blue["B_fighter"].append(data_M_red["R_fighter"])

ranking_M = data_M_winners.value_counts()[:10]

data_F = df.loc[df["gender"] == "FEMALE"]
data_F_blue = data_F.loc[df["Winner"] == "Blue"]
data_F_red = data_F.loc[df["Winner"] == "Red"]
data_F_winners = data_F_blue["B_fighter"].append(data_F_red["R_fighter"])

ranking_F = data_F_winners.value_counts()[:10]


# Top 10 geral Feminino e Masculino (mais disputas)
data_M = df.loc[df["gender"] == "MALE"]
data_M_fighters = data_M["B_fighter"].append(data_M["R_fighter"])

male_most_fights =  data_M_fighters.value_counts()[:10]

data_F = df.loc[df["gender"] == "FEMALE"]
data_F_fighters = data_F["B_fighter"].append(data_F["R_fighter"])
female_most_fights =  data_F_fighters.value_counts()[:10]

#Distribuição do número de vitórias por lutadores
dist_M = data_M_winners.value_counts().value_counts().sort_index(ascending = False)
dist_F = data_F_winners.value_counts().value_counts().sort_index(ascending = False)



#Altura e peso médio

#peso médio em kilos

class_weight = { "Flyweight": 0, "Bantamweight": 0, "Featherweight": 0, "Lightweight": 0,"Welterweight": 0, "Middleweight": 0, "Light Heavyweight": 0, "Heavyweight": 0,  "Women's Strawweight": 0, "Women's Flyweight": 0, "Women's Bantamweight": 0, "Women's Strawweight": 0, "Women's Featherweight": 0}

for weight in class_weight.keys():
    data = df[df['weight_class'].str.contains(rf'^{weight}')]
    total_weight = data["B_Weight_lbs"].append(data["R_Weight_lbs"])
    mean = total_weight.mean()
    mean *= 0.454 #converte de libras para kilogramas
    class_weight[weight] = round(mean, 2)

#altura média em m
class_height = { "Flyweight": 0, "Bantamweight": 0, "Featherweight": 0, "Lightweight": 0,"Welterweight": 0, "Middleweight": 0, "Light Heavyweight": 0, "Heavyweight": 0,  "Women's Strawweight": 0, "Women's Flyweight": 0, "Women's Bantamweight": 0, "Women's Strawweight": 0, "Women's Featherweight": 0}
for height in class_height.keys():
    data = df[df['weight_class'].str.contains(rf'^{height}')]
    total_height = data["B_Height_cms"].append(data["R_Height_cms"])
    mean = total_height.mean()
    class_height[height] = round(mean / 100, 2)
    
    
# Como a luta terminou (com e sem torcida)

#com torcida

data_torcida = df.loc[df["empty_arena"] == False]["finish"].value_counts()

torcida_decision = int(data_torcida["U-DEC"]) + int(data_torcida["S-DEC"]) + int(data_torcida["M-DEC"])
torcida_submission = int(data_torcida["SUB"])
torcida_knockout = int(data_torcida["KO/TKO"])
torcida_total = torcida_decision + torcida_submission + torcida_knockout

torcida = {"DEC": round(torcida_decision / torcida_total, 2), "SUB": round(torcida_submission / torcida_total, 2), "KO/TKO": round(torcida_knockout / torcida_total, 2)}
print("Como a luta terminou, com torcida)")
print(torcida)

#sem torcida

data_vazio = df.loc[df["empty_arena"] == True]["finish"].value_counts()

vazio_decision = int(data_vazio["U-DEC"]) + int(data_vazio["S-DEC"]) + int(data_vazio["M-DEC"])
vazio_submission = int(data_vazio["SUB"])
vazio_knockout = int(data_vazio["KO/TKO"])
vazio_total = vazio_decision + vazio_submission + vazio_knockout

torcida = {"DEC": round(vazio_decision / vazio_total, 2), "SUB": round(vazio_submission / vazio_total, 2), "KO/TKO": round(vazio_knockout / vazio_total, 2)}
print("Como a luta terminou, sem torcida)")
print(torcida)






    
    
    









    
    
    
    