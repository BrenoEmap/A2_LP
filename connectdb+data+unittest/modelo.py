#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:01:00 2020

@author: luis
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt
import re
from scipy import stats
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2


df = pd.read_csv("ufc.csv")


dropdata = df.drop(["date","location","country","title_bout","empty_arena", "constant_1", "B_match_weightclass_rank", "R_match_weightclass_rank", "R_Womens_Flyweight_rank", "R_Womens_Featherweight_rank", "R_Womens_Strawweight_rank", "R_Womens_Bantamweight_rank", "R_Heavyweight_rank",	"R_Light_Heavyweight_rank", "R_Middleweight_rank", "R_Welterweight_rank", "R_Lightweight_rank", "R_Featherweight_rank", "R_Bantamweight_rank",	"R_Flyweight_rank", "R_PoundforPound_rank", "B_Womens_Flyweight_rank", "B_Womens_Featherweight_rank","B_Womens_Strawweight_rank", "B_Womens_Bantamweight_rank", "B_Heavyweight_rank", "B_Light_Heavyweight_rank",	"B_Middleweight_rank", "B_Welterweight_rank", "B_Lightweight_rank",	"B_Featherweight_rank",	"B_Bantamweight_rank",	"B_Flyweight_rank",	"B_PoundforPound_rank","better_rank", "finish", "finish_details"], axis = 1)
dropdata = dropdata.loc[dropdata["gender"] == "MALE"]

inverse = dropdata.rename(columns={"B_avg_SIG_STR_landed":  "R_avg_SIG_STR_landed", "R_avg_SIG_STR_landed": "B_avg_SIG_STR_landed", "R_avg_SUB_ATT": "B_avg_SUB_ATT", "B_avg_SUB_ATT": "R_avg_SUB_ATT", "B_avg_TD_landed": "R_avg_TD_landed", "R_avg_TD_landed": "B_avg_TD_landed"})

# Vencedores dão mais golpes do que perdedores?

vXp = dropdata.loc[dropdata["Winner"] == "Blue"][["B_avg_SIG_STR_landed", "R_avg_SIG_STR_landed"]].append(inverse.loc[inverse["Winner"] == "Red"][["B_avg_SIG_STR_landed", "R_avg_SIG_STR_landed"]])
vXp = vXp.dropna()

sns.jointplot(vXp["R_avg_SIG_STR_landed"], vXp["B_avg_SIG_STR_landed"], kind="reg", stat_func=r2)

# plt.show()


# Obtivemos um R2 muito baixo (0.15), logo, essa relação está longe de ser suficiente


# talvez se somarmos todas as estatísticas de ataques em só uma coluna?
vXp2 = dropdata.loc[dropdata["Winner"] == "Blue"][["B_avg_SIG_STR_landed", "R_avg_SIG_STR_landed", "R_avg_SUB_ATT", "B_avg_SUB_ATT", "R_avg_TD_landed", "B_avg_TD_landed"]].append(inverse.loc[inverse["Winner"] == "Red"][["B_avg_SIG_STR_landed", "R_avg_SIG_STR_landed", "R_avg_SUB_ATT", "B_avg_SUB_ATT", "R_avg_TD_landed", "B_avg_TD_landed"]])
vXp2["Vencedor"] = vXp2["B_avg_SIG_STR_landed"] + vXp2["B_avg_SUB_ATT"] + vXp2["B_avg_TD_landed"]
vXp2["Perdedor"] = vXp2["R_avg_SIG_STR_landed"] + vXp2["R_avg_SUB_ATT"] + vXp2["R_avg_TD_landed"]
vXp2 = vXp2.dropna()

sns.jointplot(vXp2["Perdedor"], vXp2["Vencedor"], kind="reg", stat_func=r2)


# vamos fazer uma matriz de correlação com características da carreira do lutador


bluewinner_data = pd.concat([dropdata, (dropdata['Winner'] == 'Blue').astype(int)], axis=1)
bluewinner_data = bluewinner_data.drop(["R_odds", "B_odds", "R_ev", "B_ev", "R_kd_bout",	"B_kd_bout", "R_sig_str_landed_bout","B_sig_str_landed_bout", "R_sig_str_attempted_bout", "B_sig_str_attempted_bout", "R_sig_str_pct_bout", "B_sig_str_pct_bout",	"R_tot_str_landed_bout","B_tot_str_landed_bout", "R_tot_str_attempted_bout", "B_tot_str_attempted_bout","R_td_landed_bout", "B_td_landed_bout", "R_td_attempted_bout", "B_td_attempted_bout", "R_td_pct_bout", "B_td_pct_bout", "R_sub_attempts_bout", "B_sub_attempts_bout", "R_pass_bout", "B_pass_bout", "R_rev_bout", "B_rev_bout"], axis = 1)
corr = bluewinner_data.corr().fillna(0)


corr2 = corr['Winner'].copy()
corr2.sort_values(inplace=True, ascending=False)
print("Lista das características melhor relacionadas ao vencedor, ordenadas de maneira descendente/n")
print(corr2)
print()
print("As principais características da carreira dos lutadores, positivamente correlacionadas com uma vitória do Azul")
print(corr2.iloc[1:6])
print()
print("As principais características da carreira dos lutadores, negativamente correlacionadas com uma vitória do Azul")
print(corr2.iloc[-5 : ])

# A diferença de idade, a idade do perdedor, a diferença no momentum dos lutadores, a diferença do número de derrotas na carreira e a diferença de takedowns aparece mais bem correlacionados positivamente com a vitória do Azul.
# A idade do azul, a média de porcentagem de golpes significativos do perdedor, a média de porcentagem de takedowns do perdedor, o momentum do perdedor, a média de takedowns acertados aparecem negativamente correlacionados à vitória do azul.


#Nós podemos utilizar dessas informações, fazendo um preditor simples, utilizando-se desses pesos.

# façamos o mesmo para o vermelho ganhador

redwinner_data = pd.concat([dropdata, (dropdata['Winner'] == 'Red').astype(int)], axis=1)
redwinner_data = redwinner_data.drop(["R_odds", "B_odds", "R_ev", "B_ev", "R_kd_bout",	"B_kd_bout", "R_sig_str_landed_bout","B_sig_str_landed_bout", "R_sig_str_attempted_bout", "B_sig_str_attempted_bout", "R_sig_str_pct_bout", "B_sig_str_pct_bout",	"R_tot_str_landed_bout","B_tot_str_landed_bout", "R_tot_str_attempted_bout", "B_tot_str_attempted_bout","R_td_landed_bout", "B_td_landed_bout", "R_td_attempted_bout", "B_td_attempted_bout", "R_td_pct_bout", "B_td_pct_bout", "R_sub_attempts_bout", "B_sub_attempts_bout", "R_pass_bout", "B_pass_bout", "R_rev_bout", "B_rev_bout"], axis = 1)
corr3 = redwinner_data.corr().fillna(0)

corr4 = corr['Winner'].copy()
corr4.sort_values(inplace=True, ascending=False)
print("Lista das características melhor relacionadas ao vencedor, ordenadas de maneira descendente/n")
print(corr4)
print()
print("As principais características da carreira dos lutadores, positivamente correlacionadas com uma vitória do Vermelho")
print(corr4.iloc[1:6])
print()
print("As principais características da carreira dos lutadores, negativamente correlacionadas com uma vitória do Vermelho")
print(corr4.iloc[-5 : ])


def preditor(blue_fighter, red_fighter):
    data_blue = dropdata.loc[dropdata["R_fighter"] == blue_fighter].append(dropdata.loc[dropdata["B_fighter"] == blue_fighter]).iloc[0]
    data_red = dropdata.loc[dropdata["R_fighter"] == red_fighter].append(dropdata.loc[dropdata["B_fighter"] == red_fighter]).iloc[0]
    result_blue = 0
    result_red = 0
    print(data_blue)
    print(data_red)
    if data_blue["R_fighter"] == blue_fighter:
        for i in corr4[1:].index:
            if not np.isnan(data_blue[i] * corr4[i]):
                result_blue += data_blue[i] * corr4[i]
              
    if data_blue["B_fighter"] == blue_fighter:
        for i in corr2[1:].index:
            if not np.isnan(data_blue[i] * corr2[i]):
                result_blue += data_blue[i] * corr2[i]
    if data_red["R_fighter"] == red_fighter:
        for i in corr4[1:].index:
            if not np.isnan(data_red[i] * corr4[i]):
                result_red += data_red[i] * corr4[i]
    if data_red["B_fighter"] == red_fighter:
        for i in corr2[1:].index:
            if not np.isnan(data_red[i] * corr2[i]):
                result_red += data_red[i] * corr2[i]
    if result_red > result_blue:
        print(f"Prevemos que o lutador {red_fighter} ganhe.")
    if result_red < result_blue:
        print(f"Prevemos que o lutador {blue_fighter} ganhe.")
    if result_red == result_blue:
        print("Não faremos previsões para essa luta")
        
            




    
    