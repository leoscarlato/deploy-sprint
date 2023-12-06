import json
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import pickle
# from ..scripts.script_data_basico import tratamento_classificacao
import sys
sys.path.append('..')
from scripts.script_data_regressao import tratamento_regressao
from scripts.script_data_classificacao import tratamento_classificacao

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




colunas_df_total   = ['idade', 'done_activities_count', 'start_of_service',
       'Qde Todos Atendimentos', 'Faltas Todos Atendimento', 'Físico',
       'Psicológico', 'Social', 'Ambiental', 'Mensagens Inbound',
       'Mensagens Outbound', 'Ligações Inbound', 'Ligações Outbound',
       'Qde Total de Tentativas de Cobrança', 'Valor Total Inadimplência',
       'Tem Problema em Aberto', 'Tempo Última Mensagem Inbound',
       'Tempo Última Mensagem Outbound', 'Target', 'id_gender_63.0',
       'id_gender_64.0', 'id_gender_Outros', 'id_marrital_status_80.0',
       'id_marrital_status_82.0', 'id_marrital_status_83.0',
       'id_health_plan_412.0', 'id_health_plan_415.0', 'id_health_plan_418.0',
       'id_health_plan_435.0', 'id_health_plan_Outros', 'notes_count_0',
       'notes_count_1', 'notes_count_2', 'notes_count_3', 'notes_count_4',
       'notes_count_5', 'notes_count_6',
       'Método de Pagamento_Cartão de crédito', 'Método de Pagamento_Dinheiro',
       'Método de Pagamento_Outros', 'Qde Total de Faturas Inadimpletes_False',
       'Qde Total de Faturas Inadimpletes_True',
       'Quem Enviou Última Mensagem_Cliente',
       'Quem Enviou Última Mensagem_Empresa']



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

        df2['Target'] = 0 # Tirar quando erik fazer o commit do novo script
        df2['id_person'] = 0
        
        model_data = df2.copy()

        model_data = tratamento_regressao(model_data)[0]
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


#Rota para calssificação 
@app.route('/classification/predict', methods=['POST'])
def class_predict():

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

        df2['id_person'] = 0
        df2['Tempo até Sair'] = 0
        
        model_data = df2.copy()


        model_data = tratamento_classificacao(model_data)
        print("aaaaaaddddddddddddddddddddddd")

        modelo_carregado = joblib.load("../modelos/classification_model.joblib")

        print('a' * 20)
        print(model_data)

        #dropar coluna Tempo até Sair de model_data

        print('b' * 20)


        model_data = model_data.drop('Target', axis=1)

        model_data = model_data.iloc[-1]
        #model data to dataframe trsnposed
        # colunas_p = pd.DataFrame(model_data)

        # print(colunas_p.T.columns == colunas_df_total)

        prediction = modelo_carregado.predict(model_data.to_numpy().reshape(1, -1))
        print(prediction)
        return jsonify({'prediction': str(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# Exemplo de request

# {"features" : {"birthdate":42.0,"id_gender":"64.0","id_marrital_status":82.0,"id_health_plan":"Outros","notes_count":0,"done_activities_count":5,"start_of_service":61.0,"Qde Todos Atendimentos":2,"Faltas Todos Atendimento":2,"F\u00edsico":3.0,"Psicol\u00f3gico":2.0,"Social":2.0,"Ambiental":3.0,"Mensagens Inbound":50.0,"Mensagens Outbound":45.0,"Liga\u00e7\u00f5es Inbound":0.0,"Liga\u00e7\u00f5es Outbound":0.0,"Qde Total de Tentativas de Cobran\u00e7a":1.0,"M\u00e9todo de Pagamento":"Cart\u00e3o de cr\u00e9dito","Qde Total de Faturas Inadimpletes":false,"Valor Total Inadimpl\u00eancia":0.0,"Tem Problema em Aberto":1,"Tempo \u00daltima Mensagem Inbound":39.0,"Tempo \u00daltima Mensagem Outbound":39.0,"Quem Enviou \u00daltima Mensagem":"Empresa"}}





