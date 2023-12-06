import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import script_data_basico
import importlib
from datetime import datetime

#importando os dataframes
df_agosto = pd.read_csv('../data/Agosto/Ana Health_Tabela Modelo Previsão Churn - Tabela até 08_23.csv', skiprows=1)
df_julho = pd.read_csv('../data/Julho/Ana Health_Tabela Modelo Previsão Churn - Tabela até 07_23.csv', skiprows=1)
df_junho = pd.read_csv('../data/Junho/Ana Health_Tabela Modelo Previsão Churn - Tabela até 06_23.csv', skiprows=1)
df_novembro = pd.read_csv('../data/Novembro/Ana Health_Tabela Modelo Previsão Churn - Tabela Geral.csv', skiprows=1)
df_outubro = pd.read_csv('../data/Outubro/Ana Health_Tabela Modelo Previsão Churn - Tabela até 10_23.csv', skiprows=1)
df_setembro = pd.read_csv('../data/Setembro/Ana Health_Tabela Modelo Previsão Churn - Tabela até 09_23.csv', skiprows=1)

#carregando o script de tratamento
importlib.reload(script_data_basico)
tratamento = script_data_basico.tratamento

fim_junho = datetime(2023, 6, 30)
fim_julho = datetime(2023, 7, 31)
fim_agosto = datetime(2023, 8, 31)
fim_setembro = datetime(2023, 9, 30)
fim_outubro = datetime(2023, 10, 31)
fim_novembro = datetime(2023, 11, 30)

#aplicando o tratamento basico para todos os meses
df_agosto = tratamento(df_agosto, fim_agosto, df_setembro)
df_julho = tratamento(df_julho, fim_julho, df_agosto)
df_junho = tratamento(df_junho, fim_junho, df_julho)
df_outubro = tratamento(df_outubro, fim_outubro, df_novembro)
df_setembro = tratamento(df_setembro,   fim_setembro, df_outubro)

#concatenando os meses em um dataframe só
df_total = pd.concat([df_junho, df_julho, df_agosto, df_setembro, df_outubro])
df_total['Target'] = df_total['status_prox_mes'] == 'won'

#salvando o dataframe
df_api = df_total.copy()
df_api = df_api.drop(['id_person', 'Target'], axis=1)
df_api.to_csv('../data/df_total.csv', index=False)


