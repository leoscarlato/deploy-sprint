import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime


def ultima_mensagem(x,y):
    if (y == None):
        return "Cliente"
    
    if x>y:
        return "Cliente"
    
    else:
        return "Empresa"
    

def lastStatus(x):
    s = x.split(';')
    return s[-1].strip()

def converte_para_horas(x):
    if pd.isnull(x):
        return None
    return int(x)/3600

def first_date(x):
    if pd.isnull(x):
        return x
    s = x.split(';')
    return s[0].strip()


def devolve_media(x):
    if pd.isnull(x):
        return None
    else:
        try:
            x = x.replace(',','.').replace('FALSE', '0')
            s = x.split(';')
            s = [float(i) for i in s]
            return np.mean(s)
        except Exception as e:
            print(f"Erro: {e}")
            return None



def tem_ou_nao(x):
    if pd.isnull(x) :
        return 0
    return 1

def retornaTempo(x,y):
    if y==None:
        return None
    
    return (y-x).days


def lost_reason_lost(x,y):
    if pd.isnull(x) or pd.isnull(y):
        return None
    
    if x == 'won':
        return None
    
    s = y.split(';')
    return s[-1].strip()

def tratamento(df):

    df = df[df['id_person'] != 'FALSE']

    colunas = ['state', 'city', 'postal_code', 'id_person_recommendation', 'Recebe Comunicados?', 'Interesses', 'Pontos de Atenção',
            'id_stage', 'id_org', 'status.1', 'activities_count', 'Qde Todos Atendimentos', 'Faltas Todos Atendimento', 'Datas Atendimento Médico',
            'Datas Acolhimento', 'Datas Psicoterapia','Qde Prescrições', 'Datas Prescrição', 'Qde Respostas WHOQOL']
    df = df.drop(colunas, axis=1)

    df['status'] = df['status'].dropna().apply(lastStatus)

    df['start_of_service'] = df['start_of_service'].apply(first_date)

    df['status'] = df['status'].dropna().apply(lastStatus)



    df['lost_reason'] = df.apply(lambda row: lost_reason_lost(row['status'], row['lost_reason']), axis=1)


    colunas_whoqol = ['Físico', 'Psicológico', 'Social', 'Ambiental']
    for coluna in colunas_whoqol:
        df[coluna] = df[coluna].apply(devolve_media)


    colunas_de_data = ['start_of_service', 'lost_time', 'add_time', 'won_time', 'lost_time.1']
    colunas_seg = ['stay_in_pipeline_stages_welcome','stay_in_pipeline_stages_first_meeting', 'stay_in_pipeline_stages_whoqol']
    #converter a coluna de segundos para horas
    
    for coluna in colunas_seg:
        df[coluna] = df[coluna].apply(converte_para_horas)

    df = df.drop(colunas_seg, axis=1)

    #Trocar a data pelo tempo em dias ate o dia de hoje
    for coluna in colunas_de_data:
        df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
        df[coluna] = df[coluna].apply(lambda x: (datetime.now() - x).days)

    df['contract_end_date'] = pd.to_datetime(df['contract_end_date'])
    df['contract_start_date'] = pd.to_datetime(df['contract_start_date'])
    
    df['Tempo até Sair'] = df.apply(lambda row: retornaTempo(row['contract_start_date'], row['contract_end_date']), axis=1)

    df['Problemas Abertos'] = df['Problemas Abertos'].apply(tem_ou_nao)
    df_simple = df[df['status'].isin(['won', 'lost'])]
    f1 = df_simple[(df_simple['status'] == 'won') & (df_simple['contract_end_date'].isna())] 
    f2 = df_simple[(df_simple['status'] == 'lost') & (df_simple['contract_end_date'].notna())] 

    df_simple = pd.concat([f1, f2])

    df_simple['contract_start_date'] = pd.to_datetime(df_simple['contract_start_date'])
    df_simple = df_simple.sort_values(by=['contract_start_date'])

    # df_aux = df_simple[df_simple['Data Última Mensagens Inbound'].notnull()]

    df_simple['Data Última Mensagens Inbound'] = pd.to_datetime(df_simple['Data Última Mensagens Inbound'])
    df_simple['Data Última Mensagens Outbound'] = pd.to_datetime(df_simple['Data Última Mensagens Outbound'])
    df_simple['Tempo Última Mensagem Inbound'] = df_simple['Data Última Mensagens Inbound'].apply(lambda x: (datetime.now() - x).days)
    df_simple['Tempo Última Mensagem Outbound'] = df_simple['Data Última Mensagens Outbound'].apply(lambda x: (datetime.now() - x).days)

    colunas_data_mensagem = ['Data Última Mensagens Inbound','Data Última Mensagens Outbound']

    df_simple = df_simple.drop(colunas_data_mensagem, axis=1)

    df_simple['Quem Enviou Última Mensagem'] = df_simple.apply(lambda row: ultima_mensagem(row['Tempo Última Mensagem Inbound'], row['Tempo Última Mensagem Outbound']), axis=1)
    
    df_simple['birthdate'] = pd.to_datetime(df_simple['birthdate'], errors='coerce')
    df_simple['birthdate'] = df_simple['birthdate'].apply(lambda x: (datetime.now() - x).days//365)
    

    return df_simple
