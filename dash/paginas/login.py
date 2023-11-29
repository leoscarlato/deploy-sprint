import streamlit as st
import bcrypt
import sqlite3

def verifica_usuario(email, senha):
    # Conectar ao banco de dados
    conn = sqlite3.connect('dash/db/database.db')
    cursor = conn.cursor()

    try:
        # Verificar se o usuário existe no banco de dados
        cursor.execute("""
        SELECT * FROM users
        WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        if user:
            stored_password_hash = user[1]
            if isinstance(stored_password_hash, str):
                stored_password_hash = stored_password_hash.encode('utf-8')
            
            if bcrypt.checkpw(senha.encode('utf-8'), stored_password_hash):
                conn.close()
                return True
            else:
                conn.close()
                return False
        else:
            conn.close()
            return False
        
    except ValueError as e:
        conn.close()
        return False

def login():
    st.title("Login")
    
    email = st.text_input("Email", key="email_login")
    password = st.text_input("Password", type="password", key="password_login")
    submit = st.button("Login")

    if submit:
        if verifica_usuario(email, password):
            st.success("Login realizado com sucesso!")
            return True
        else:
            st.error("Erro ao realizar login!")
            return False