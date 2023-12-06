
import streamlit as st
from cadastro import cadastro
from login import login
from streamlit_option_menu import option_menu
from dashboard import dashboard
import pandas as pd
from script_dataframe import tratamento
from pymongo import MongoClient




def connect_to_mongodb():
    client = MongoClient(st.secrets.mongo.mongo_uri)
    db = client[st.secrets.mongo.mongo_db]
    return db

# Inicializando o estado de login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Initialize df in session state
if 'df' not in st.session_state:
    st.session_state['df'] = None

if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False

def main():
    st.set_page_config(page_title="Dash", page_icon="📊", layout="wide")

    # Mostrar as opções de login e cadastro fora da barra lateral
    if not st.session_state['logged_in']:
        tab_login, tab_cadastro = st.tabs(["Login", "Cadastro"])

        with tab_login:
            if login():
                st.session_state['logged_in'] = True
                st.rerun()  # Reinicia o aplicativo para atualizar a navegação

        with tab_cadastro:
            cadastro()

    # Configurar a barra lateral para navegação após o login
    if st.session_state['logged_in']:
        with st.sidebar:

            st.title(f"Olá, {st.session_state['user_name']}! 👋")

            arquivo_upload = st.file_uploader("", type="csv")

            if arquivo_upload is not None:
                df = pd.read_csv(arquivo_upload, header=1)
                df = tratamento(df)
                st.session_state.df = df
                st.session_state['file_uploaded'] = True

            if arquivo_upload is None and st.session_state['df'] is None:
                st.error("Carregue um arquivo CSV para ver o dashboard.")

            elif arquivo_upload is None and st.session_state['file_uploaded']:
                st.session_state['df'] = None
                st.session_state['file_uploaded'] = False
                
            if st.session_state['df'] is not None:
                try:
                    st.markdown("---")
                    # Definindo os valores padrão para os inputs de data
                    default_data_inicial = st.session_state.df['contract_start_date'].min()
                    default_data_final = st.session_state.df['contract_end_date'].max()

                    st.session_state['data_inicial'] = st.date_input(
                        "Data inicial", 
                        value=st.session_state.get('data_inicial', default_data_inicial), 
                        min_value=default_data_inicial, 
                        max_value=default_data_final
                    )
                    st.session_state['data_final'] = st.date_input(
                        "Data final", 
                        value=st.session_state.get('data_final', default_data_final), 
                        min_value=default_data_inicial, 
                        max_value=default_data_final
                    )

                    # Botão para resetar os filtros de data
                    if st.button("Resetar filtros de data"):
                        st.session_state['data_inicial'] = default_data_inicial
                        st.session_state['data_final'] = default_data_final
                        st.rerun()

                except Exception as e:
                    st.error(f"Erro ao carregar filtros de data: {e}")

            st.markdown("---")

             # Botão de logout
            if st.sidebar.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['df'] = None

                try:
                    db = connect_to_mongodb()
                    # Insere o log de logout
                    auth_logs = db.auth_logs
                    auth_logs.insert_one({
                        "username": st.session_state['user_name'],
                        "time": pd.to_datetime("now"),
                        "type": "logout"
                    })

                except Exception as e:
                    st.error(f"Erro ao conectar ao banco de dados: {e}")

                st.experimental_rerun()

        dashboard()

if __name__ == "__main__":
    main()