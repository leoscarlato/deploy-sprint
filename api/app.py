import json
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import pickle
import pathlib
app = Flask(__name__)

categorical_columns = ['MS.SubClass',
 'MS.Zoning',
 'Land.Contour',
 'Lot.Config',
 'Neighborhood',
 'Bldg.Type',
 'House.Style',
 'Roof.Style',
 'Mas.Vnr.Type',
 'Foundation',
 'Bsmt.Qual',
 'Bsmt.Cond',
 'Bsmt.Exposure',
 'BsmtFin.Type.1',
 'BsmtFin.Type.2',
 'Central.Air',
 'Garage.Type',
 'Garage.Finish',
 'Sale.Type',
 'Sale.Condition',
 'Condition',
 'Exterior']

ordinal_columns = ['Lot.Shape',
 'Land.Slope',
 'Overall.Qual',
 'Overall.Cond',
 'Exter.Qual',
 'Exter.Cond',
 'Heating.QC',
 'Electrical',
 'Kitchen.Qual',
 'Functional',
 'Paved.Drive',
 'Fence']

DATA_DIR = pathlib.Path.cwd().parent / 'data'
print(DATA_DIR)

clean_data_path = DATA_DIR / 'processed' / 'ames_clean.pkl'

@app.route('/predict', methods=['POST'])
def predict():

    try:
        data = request.get_json()
        features = data.get('features')
        
        if not features:
            return jsonify({'error': 'Dados de entrada não fornecidos'}), 400

        features = pd.DataFrame(features, index=[0])

        with open("data/processed/ames_clean.pkl", 'rb') as file:
            data_ames = pickle.load(file)


        data_ames2 = data_ames.copy()
        data_ames2 = pd.concat([data_ames2, features], ignore_index=False)
        model_data = data_ames2.copy()

        for col in ordinal_columns:
            codes, _ = pd.factorize(data_ames2[col], sort=True)
            model_data[col] = codes

        model_data = pd.get_dummies(model_data, drop_first=True)
        print(model_data.info())
        for cat in categorical_columns:
            dummies = []
            for col in model_data.columns:
                if col.startswith(cat + "_"):
                    dummies.append(f'"{col}"')
            dummies_str = ', '.join(dummies)
            print(f'From column "{cat}" we made {dummies_str}\n')

        modelo_carregado = joblib.load("notebooks/regression_model.joblib")
        model_data = model_data.iloc[-1]
        print(model_data)

        model_data = model_data.drop('SalePrice')
        prediction = modelo_carregado.predict(model_data.to_numpy().reshape(1, -1))
        print(prediction)
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
