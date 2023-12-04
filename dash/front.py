import streamlit as st
from paginas.cadastro import cadastro
from paginas.login import login
from streamlit_option_menu import option_menu
from paginas.dashboard import dashboard
import pandas as pd
from script_dataframe import tratamento
import sqlite3

db_path = 'db/database.db'

# Inicializando o estado de login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Initialize df in session state
if 'df' not in st.session_state:
    st.session_state['df'] = None

if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False  # Flag para controlar a exibição das opções de data

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
            st.header(f"Olá, {st.session_state['user_name']}! 👋")

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
                    st.session_state['data_inicial'] = st.date_input(
                        "Data inicial", 
                        value=st.session_state.df['contract_start_date'].min(), 
                        min_value=st.session_state.df['contract_start_date'].min(), 
                        max_value=st.session_state.df['contract_start_date'].max()
                    )
                    st.session_state['data_final'] = st.date_input(
                        "Data final", 
                        value=st.session_state.df['contract_end_date'].max(), 
                        min_value=st.session_state.df['contract_end_date'].min(), 
                        max_value=st.session_state.df['contract_end_date'].max()
                    )
                except Exception as e:
                    st.error(f"Erro ao carregar filtros de data: {e}")
            st.markdown("---")

            # Botão de logout fora do bloco condicional do df
            if st.sidebar.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['df'] = None
                
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO auth_logs (username, time, type)
                VALUES (?, datetime('now'), 'logout')
                """, (st.session_state['user_name'],))

                conn.commit()
                conn.close()



                st.experimental_rerun()  # Reinicia o aplicativo para atualizar a navegação
            
        dashboard()
        

if __name__ == "__main__":
    main()