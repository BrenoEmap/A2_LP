"""Módulo de refinamento da base de dados do UFC

"""

import pandas as pd
from connectdb import data_ufc

df = data_ufc

#df.columns.get_loc('nome da coluna') -> retorna a localização
#----------------------
#df.loc[df['date'] == data desejada, [colunas desejadas]]
#pra condições variadas, o lado a esquerda da virgula deve ter cada condições
#entre parenteses e separadas por '&'.
#----------------------
#country_df = df['country']
#----------------------
#df['nome da coluna'].value_counts() -> retorna a quantidade de vezes que
#um valor aparece
#----------------------
#
# EndOfFight = df.loc[:,['date',
#                        'B_win_by_Decision_Majority', 'R_win_by_Decision_Majority','B_win_by_Decision_Split', 'R_win_by_Decision_Split', 'B_win_by_Decision_Unanimous', 'R_win_by_Decision_Unanimous',
#                        'B_win_by_KOTKO', 'R_win_by_KOTKO',
#                        'B_win_by_Submission', 'R_win_by_Submission',
#                        'B_win_by_TKO_Doctor_Stoppage', 'R_win_by_TKO_Doctor_Stoppage']]

# EndOfFight['Win_by_Decision'] = EndOfFight['B_win_by_Decision_Majority'] + EndOfFight['R_win_by_Decision_Majority'] 
# + EndOfFight['B_win_by_Decision_Split'] + EndOfFight['R_win_by_Decision_Split']
# + EndOfFight['B_win_by_Decision_Unanimous'] + EndOfFight['R_win_by_Decision_Unanimous']

# EndOfFight['Win_by_KOTKO'] = EndOfFight['B_win_by_KOTKO'] + EndOfFight['R_win_by_KOTKO']

# EndOfFight['Win_by_Submission'] = EndOfFight['B_win_by_Submission'] + EndOfFight['R_win_by_Submission']

# EndOfFight['Doctor_Stoppage'] = EndOfFight['B_win_by_TKO_Doctor_Stoppage'] + EndOfFight['R_win_by_TKO_Doctor_Stoppage']

# EndOfFight = EndOfFight.loc[:, ['date','Win_by_Decision','Win_by_KOTKO','Win_by_Submission','Doctor_Stoppage']]



