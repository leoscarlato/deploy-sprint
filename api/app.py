import json
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import pickle
# from ..scripts.script_data_basico import tratamento_classificacao
import sys
sys.path.append('..')
from scripts.script_data_regressao import tratamento_regressao
# from ..scripts.script_data_regressao import tratamento_regressao

def transform_to_category(x,qtd_itens,lista_itens):
   for i in range(qtd_itens):
      if x == lista_itens[i]:
         return str(x)
   return 'Outros'

def retornaTempo(x,y):
    if y==None:
        return None
    
    return (y-x).days

app = Flask(__name__)


colunas_dropadas_regr = ['contract_start_date','contract_end_date','id_continuity_pf','Canal de Preferência','status','lost_time','add_time','id_label','won_time','lost_time.1','lost_reason','lost_reason.1',\
                     'Qde Atendimento Médico','Faltas Atendimento Médico',	'Qde Atendimentos Acolhimento',	'Faltas Acolhimento',	'Qde Psicoterapia',	'Faltas Psicoterapia','Data Última Ligações Outbound',\
                     'Data Última Ligações Inbound','Qde Total de Faturas Pagas após Vencimento','Qde Perfis de Pagamento Inativos', 'Valor Médio da Mensalidade', 'status_prox_mes', 'Qde Total de Faturas','Problemas Abertos', "Tempo até Sair"]

# #rota para classificação
# @app.route('/classification/predict', methods=['POST'])
# def predict_class():

#     try:
#         data = request.get_json()
#         features = data.get('features')
        
#         if not features:
#             return jsonify({'error': 'Dados de entrada não fornecidos'}), 400

#         features = pd.DataFrame(features, index=[0])

#         print(features.iloc[0])-

#         print("#"*20)

#         clean_data_path = "../data/df_total.csv"

#         df = pd.read_csv(clean_data_path)
#         df = df.drop(colunas_dropadas_regr, axis=1)
#         df2 = df.copy()

#         features = features[df2.columns]

#         df2 = pd.concat([df2, features], ignore_index=False)
#         model_data = df2.copy()

#         model_data = tratamento_classificacao(model_data)

#         model_data = model_data.iloc[-1]
#         print(model_data)

#         modelo_carregado = joblib.load("../notebooks/regression_model.joblib")

#         # model_data = model_data.drop('SalePrice')
#         prediction = modelo_carregado.predict(model_data.to_numpy().reshape(1, -1))
#         print(prediction)
#         return jsonify({'prediction': prediction[0]})



#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


#Rota para regressão
@app.route('/regression/predict', methods=['POST'])
def predict():

    try:
        data = request.get_json()
        features = data.get('features')
        
        if not features:
            return jsonify({'error': 'Dados de entrada não fornecidos'}), 400

        features = pd.DataFrame(features, index=[0])

        print(features.iloc[0])

        print("#"*20)

        clean_data_path = "../data/df_total.csv"

        df = pd.read_csv(clean_data_path)
        # df = df.drop(colunas_dropadas_regr, axis=1)
        df2 = df.copy()

        # features = features[df2.columns]

        df2 = pd.concat([df2, features], ignore_index=False)

        df2['Target'] = 0
        df2['id_person'] = 0
        
        model_data = df2.copy()

        model_data = tratamento_regressao(model_data)[0]

        ##############################################
                
        # colunas_get_dummies = ['id_gender','id_marrital_status','id_health_plan','notes_count','Método de Pagamento','Qde Total de Faturas Inadimpletes', 'Quem Enviou Última Mensagem']

        # #coluna de genero
        # model_data['id_gender'] = model_data['id_gender'] = model_data['id_gender'].apply(lambda x: transform_to_category(x,2,[63,64]))
        # #coluna de estado civil
        # #drop marrital status diferentes de 80,82,83
        # model_data = model_data[model_data['id_marrital_status'].isin([80,82,83])]
        # print("a#"*20)
        # print(model_data.iloc[-1])
        # print("#"*20)


        # model_data['id_marrital_status'] = model_data['id_marrital_status'].apply(lambda x: transform_to_category(x,3,[80,82,83]))
        # #coluna de health plan
        # model_data['id_health_plan'] = model_data['id_health_plan'].apply(lambda x: transform_to_category(x,4,[412,415,418,435]))
        # #coluna de notes count
        # model_data = model_data[model_data['notes_count'] < 7]

        # #coluna birthdate
        # model_data = model_data[model_data['birthdate'].notna()]
        # #coluna de fisico
        # model_data['Físico'] = model_data['Físico'].fillna(model_data['Físico'].mean())
        # #coluna de psicologico
        # model_data['Psicológico'] = model_data['Psicológico'].fillna(model_data['Psicológico'].mean())
        # #coluna de social 
        # model_data['Social'] = model_data['Social'].fillna(model_data['Social'].mean())
        # #coluna de ambiental
        # model_data['Ambiental'] = model_data['Ambiental'].fillna(model_data['Ambiental'].mean())

        # #coluna de mensagens inbound
        # model_data['Mensagens Inbound'] = model_data['Mensagens Inbound'].fillna(0)
        # #coluna de mensagens outbound
        # model_data['Mensagens Outbound'] = model_data['Mensagens Outbound'].fillna(0)
        # #coluna de ligacoes inbound
        # model_data['Ligações Inbound'] = model_data['Ligações Inbound'].fillna(0)
        # #coluna de ligacoes outbound
        # model_data['Ligações Outbound'] = model_data['Ligações Outbound'].fillna(0)
        # #coluna qtd tentativas de cobrança
        # model_data['Qde Total de Tentativas de Cobrança'] = model_data['Qde Total de Tentativas de Cobrança'].fillna(0)

        # #coluna método de pagamento
        # model_data['Método de Pagamento'] = model_data['Método de Pagamento'].apply(lambda x: transform_to_category(x,2,["Cartão de crédito","Dinheiro"]))
        # #coluna total de faturas inadimplentes
        # model_data['Qde Total de Faturas Inadimpletes'] = model_data['Qde Total de Faturas Inadimpletes'].fillna(0)
        # model_data['Qde Total de Faturas Inadimpletes'] = model_data['Qde Total de Faturas Inadimpletes'].apply(lambda x: True if x > 0 else False)

        # #coluna valor total inadimplente
        # model_data['Valor Total Inadimplência'] = model_data['Valor Total Inadimplência'].fillna(0)
        # #coluna Tempo Última Mensagem Inbound
        # model_data['Tempo Última Mensagem Inbound'] = model_data['Tempo Última Mensagem Inbound'].fillna(0)
        # #coluna Tempo Última Mensagem Outbound
        # model_data['Tempo Última Mensagem Outbound'] = model_data['Tempo Última Mensagem Outbound'].fillna(0)
        # #rename coluna birthdate para idade
        # model_data = model_data.rename(columns={'birthdate':'idade'})

        # # dropa linhas duplicadas

        # model_data = pd.get_dummies(model_data, columns=colunas_get_dummies)

        modelo_carregado = joblib.load("../notebooks/regression_model.joblib")

        print('a' * 20)
        print(model_data)

        #dropar coluna Tempo até Sair de model_data

        model_data = model_data.drop('Tempo até Sair', axis=1)


        print('b' * 20)


        model_data = model_data.iloc[-1]
        
        print(model_data)

        # model_data = model_data.drop('SalePrice')
        prediction = modelo_carregado.predict(model_data.to_numpy().reshape(1, -1))
        print(prediction)
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# Exemplo de request

# {"features" : {"birthdate":42.0,"id_gender":"64.0","id_marrital_status":82.0,"id_health_plan":"Outros","notes_count":0,"done_activities_count":5,"start_of_service":61.0,"Qde Todos Atendimentos":2,"Faltas Todos Atendimento":2,"F\u00edsico":3.0,"Psicol\u00f3gico":2.0,"Social":2.0,"Ambiental":3.0,"Mensagens Inbound":50.0,"Mensagens Outbound":45.0,"Liga\u00e7\u00f5es Inbound":0.0,"Liga\u00e7\u00f5es Outbound":0.0,"Qde Total de Tentativas de Cobran\u00e7a":1.0,"M\u00e9todo de Pagamento":"Cart\u00e3o de cr\u00e9dito","Qde Total de Faturas Inadimpletes":false,"Valor Total Inadimpl\u00eancia":0.0,"Tem Problema em Aberto":1,"Tempo \u00daltima Mensagem Inbound":39.0,"Tempo \u00daltima Mensagem Outbound":39.0,"Quem Enviou \u00daltima Mensagem":"Empresa"}}