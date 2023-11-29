import streamlit as st
import pandas as pd
import io
from script_dataframe import tratamento

def dados():
    st.title("Dados")
    st.write("Insira os dados que deseja visualizar:")

    if 'df' not in st.session_state:
        st.session_state.df = None

    # Adicionar arquivo
    arquivo_upload = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if arquivo_upload is not None:
        # Ler o arquivo CSV em um DataFrame
        df = pd.read_csv(arquivo_upload, header=1)
        df = tratamento(df)
        st.session_state.df = df
        st.success("Arquivo carregado com sucesso!")

    if st.session_state.df is not None:
        st.dataframe(st.session_state.df)