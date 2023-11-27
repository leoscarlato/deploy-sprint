import streamlit as st
import requests

def login():
    st.title("Login")
    
    email = st.text_input("Email", key="email_login")
    password = st.text_input("Password", type="password", key="password_login")
    submit = st.button("Login")

    if submit:
        url = "http://localhost:5000/login"
        data = {"email": email, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success("Login realizado com sucesso!")
            return True
        else:
            st.error("Erro ao realizar login!")
            return False