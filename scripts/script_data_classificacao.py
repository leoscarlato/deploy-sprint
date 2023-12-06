import pandas as pd
import numpy as np

def transform_to_category(x,qtd_itens,lista_itens):
   for i in range(qtd_itens):
      if x == lista_itens[i]:
         return str(x)
   return 'Outros'


def tratamento_classificacao(df):
    df_total = df.copy()
    colunas_dropadas = ['id_person','contract_start_date','contract_end_date','id_continuity_pf','Canal de Preferência','status','lost_time','add_time','id_label','won_time','lost_time.1','lost_reason','lost_reason.1',\
                        'Qde Atendimento Médico','Faltas Atendimento Médico',	'Qde Atendimentos Acolhimento',	'Faltas Acolhimento',	'Qde Psicoterapia',	'Faltas Psicoterapia','Data Última Ligações Outbound',\
                        'Data Última Ligações Inbound','Qde Total de Faturas Pagas após Vencimento','Qde Perfis de Pagamento Inativos','Tempo até Sair', 'Valor Médio da Mensalidade', 'status_prox_mes', 'Qde Total de Faturas','Problemas Abertos']


    colunas_get_dummies = ['id_gender','id_marrital_status','id_health_plan','notes_count','Método de Pagamento','Qde Total de Faturas Inadimpletes', 'Quem Enviou Última Mensagem']

    #coluna de genero
    df_total['id_gender'] = df_total['id_gender'] = df_total['id_gender'].apply(lambda x: transform_to_category(x,2,[63,64]))
    #coluna de estado civil
    #drop marrital status diferentes de 80,82,83
    df_total = df_total[df_total['id_marrital_status'].isin([80,82,83])]
    df_total['id_marrital_status'] = df_total['id_marrital_status'].apply(lambda x: transform_to_category(x,3,[80,82,83]))
    #coluna de health plan
    df_total['id_health_plan'] = df_total['id_health_plan'].apply(lambda x: transform_to_category(x,4,[412,415,418,435]))
    #coluna de notes count
    df_total = df_total[df_total['notes_count'] < 7]


    #coluna birthdate
    df_total = df_total[df_total['birthdate'].notna()]
    #coluna de fisico
    df_total['Físico'] = df_total['Físico'].fillna(df_total['Físico'].mean())
    #coluna de psicologico
    df_total['Psicológico'] = df_total['Psicológico'].fillna(df_total['Psicológico'].mean())
    #coluna de social 
    df_total['Social'] = df_total['Social'].fillna(df_total['Social'].mean())
    #coluna de ambiental
    df_total['Ambiental'] = df_total['Ambiental'].fillna(df_total['Ambiental'].mean())
    #coluna de mensagens inbound
    df_total['Mensagens Inbound'] = df_total['Mensagens Inbound'].fillna(0)
    #coluna de mensagens outbound
    df_total['Mensagens Outbound'] = df_total['Mensagens Outbound'].fillna(0)
    #coluna de ligacoes inbound
    df_total['Ligações Inbound'] = df_total['Ligações Inbound'].fillna(0)
    #coluna de ligacoes outbound
    df_total['Ligações Outbound'] = df_total['Ligações Outbound'].fillna(0)
    #coluna qtd tentativas de cobrança
    df_total['Qde Total de Tentativas de Cobrança'] = df_total['Qde Total de Tentativas de Cobrança'].fillna(0)
    #coluna método de pagamento
    df_total['Método de Pagamento'] = df_total['Método de Pagamento'].apply(lambda x: transform_to_category(x,2,["Cartão de crédito","Dinheiro"]))
    #coluna total de faturas inadimplentes
    df_total['Qde Total de Faturas Inadimpletes'] = df_total['Qde Total de Faturas Inadimpletes'].fillna(0)
    df_total['Qde Total de Faturas Inadimpletes'] = df_total['Qde Total de Faturas Inadimpletes'].apply(lambda x: True if x > 0 else False)
    #coluna valor total inadimplente
    df_total['Valor Total Inadimplência'] = df_total['Valor Total Inadimplência'].fillna(0)
    #coluna Tempo Última Mensagem Inbound
    df_total['Tempo Última Mensagem Inbound'] = df_total['Tempo Última Mensagem Inbound'].fillna(0)
    #coluna Tempo Última Mensagem Outbound
    df_total['Tempo Última Mensagem Outbound'] = df_total['Tempo Última Mensagem Outbound'].fillna(0)
    #rename coluna birthdate para idade
    df_total = df_total.rename(columns={'birthdate':'idade'})
    # dropa linhas duplicadas

    df_total = df_total.drop_duplicates()  
    df_total = df_total.drop(colunas_dropadas, axis=1)
    df_total = pd.get_dummies(df_total, columns=colunas_get_dummies)
    return df_total