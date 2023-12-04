import streamlit as st
import bcrypt
import sqlite3

def cadastrar_usuario(email, username, password):
    # Gerar um hash da senha

    password_encoded = password.encode('utf-8')

    hashed = bcrypt.hashpw(password_encoded, bcrypt.gensalt())

    if email == "" or password == "" or username == "":
        st.error("Erro ao cadastrar usuário!")
        return False
    else:
        if "@anahealth.app" not in email:
            st.error("E-mail inválido!")
            return False
        
        # Conectar ao banco de dados
        conn = sqlite3.connect('dash/db/database.db')
        cursor = conn.cursor()
        
        # Inserir o usuário no banco de dados
        cursor.execute("""
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
        """, (username, hashed, email))

        # Criar um log de autenticação
        cursor.execute("""
        INSERT INTO auth_logs (username, time, type)
        VALUES (?, datetime('now'), 'register')
        """, (username,))

        # Salvar as alterações
        conn.commit()
        conn.close()

        st.success("Cadastro realizado com sucesso!")
        
        return True

def cadastro():
    st.title("Cadastro")
    
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.button("Cadastro")

    if submit:
        cadastrar_usuario(email, username, password)

