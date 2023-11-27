import streamlit as st
import requests

def cadastro():
    st.title("Cadastro")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.button("Cadastro")

    if submit:
        url = "http://localhost:5000/user"
        data = {"email": email, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso!")
        else:
            st.error("Erro ao cadastrar usuário!")
