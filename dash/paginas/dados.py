import streamlit as st
import pandas as pd

def dados():
    st.title("Dados")
    st.write("Insira os dados que deseja visualizar:")
    
    # adicionar arquivo
    arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv")
    if arquivo:
        st.write("Arquivo carregado com sucesso!")
        df = pd.read_csv(arquivo, header=1)
        st.dataframe(df)

        
if __name__ == "__main__":
    dados()
