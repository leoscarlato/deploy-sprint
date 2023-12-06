import json
from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import pickle
import os
from dotenv import load_dotenv

# from ..scripts.script_data_basico import tratamento_classificacao
import sys
sys.path.append('..')
from scripts.script_data_regressao import tratamento_regressao
from scripts.script_data_classificacao import tratamento_classificacao


load_dotenv()

# cliente = MongoClient(os.getenv('MONGO_URI'))
# db = cliente[os.getenv('MONGO_DB')]

def connect_mongo_db():
    cliente = MongoClient(os.getenv('MONGO_URI'))
    db = cliente[os.getenv('MONGO_DB')]
    
    return db


app = Flask(__name__)

auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)


@auth.verify_password
def verify_password(username, password):
    db = connect_mongo_db()
    user = db.users.find_one({'email': username})
    if user and bcrypt.check_password_hash(user['password'], password):
        app.logger.info("Password verification successful.")
        return username
    app.logger.info("Password verification failed.")

#Rota para regressão

@app.route('/regression/predict', methods=['POST'])
@auth.login_required
def predict():

    try:
        data = request.get_json()
        features = data.get('features')
        
        if not features:
            return jsonify({'error': 'Dados de entrada não fornecidos'}), 400

        features = pd.DataFrame(features, index=[0])



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


        #dropar coluna Tempo até Sair de model_data

        model_data = model_data.drop('Tempo até Sair', axis=1)




        model_data = model_data.iloc[-1]
        

        # model_data = model_data.drop('SalePrice')
        prediction = modelo_carregado.predict(model_data.to_numpy().reshape(1, -1))
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Rota para calssificação 
@app.route('/classification/predict', methods=['POST'])
@auth.login_required
def class_predict():

    try:
        data = request.get_json()
        features = data.get('features')
        
        if not features:
            return jsonify({'error': 'Dados de entrada não fornecidos'}), 400

        features = pd.DataFrame(features, index=[0])


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

        modelo_carregado = joblib.load("../modelos/classification_model.joblib")


        #dropar coluna Tempo até Sair de model_data



        model_data = model_data.drop('Target', axis=1)

        model_data = model_data.iloc[-1]
        #model data to dataframe trsnposed
        # colunas_p = pd.DataFrame(model_data)

        # print(colunas_p.T.columns == colunas_df_total)

        prediction = modelo_carregado.predict(model_data.to_numpy().reshape(1, -1))
        return jsonify({'prediction': str(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# Exemplo de request

# {"features" : {"birthdate":42.0,"id_gender":"64.0","id_marrital_status":82.0,"id_health_plan":"Outros","notes_count":0,"done_activities_count":5,"start_of_service":61.0,"Qde Todos Atendimentos":2,"Faltas Todos Atendimento":2,"F\u00edsico":3.0,"Psicol\u00f3gico":2.0,"Social":2.0,"Ambiental":3.0,"Mensagens Inbound":50.0,"Mensagens Outbound":45.0,"Liga\u00e7\u00f5es Inbound":0.0,"Liga\u00e7\u00f5es Outbound":0.0,"Qde Total de Tentativas de Cobran\u00e7a":1.0,"M\u00e9todo de Pagamento":"Cart\u00e3o de cr\u00e9dito","Qde Total de Faturas Inadimpletes":false,"Valor Total Inadimpl\u00eancia":0.0,"Tem Problema em Aberto":1,"Tempo \u00daltima Mensagem Inbound":39.0,"Tempo \u00daltima Mensagem Outbound":39.0,"Quem Enviou \u00daltima Mensagem":"Empresa"}}





