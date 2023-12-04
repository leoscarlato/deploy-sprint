import streamlit as st
import bcrypt
import sqlite3

def buscar_username(email):
    # Conectar ao banco de dados
    conn = sqlite3.connect('dash/db/database.db')
    cursor = conn.cursor()

    try:
        # Verificar se o usuário existe no banco de dados
        cursor.execute("""SELECT username FROM users WHERE email = ?""", (email,))
        username = cursor.fetchone()
        conn.close()
        return username[0]
    except ValueError as e:
        conn.close()
        return False

def verifica_usuario(email, senha):
    # Conectar ao banco de dados
    conn = sqlite3.connect('dash/db/database.db')
    cursor = conn.cursor()

    try:
        # Verificar se o usuário existe no banco de dados
        cursor.execute("""SELECT password FROM users WHERE email = ?""", (email,))
        user = cursor.fetchone()

        if user:
            stored_password_hash = user[0]  # Assuming password hash is in the first position
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
        
    except Exception as e:  # Catch a broader range of exceptions
        print(f"Error during authentication: {e}")  # Added for debugging

        
        conn.close()
        return False


def login():
    st.title("Login")
    
    email = st.text_input("Email", key="email_login")
    password = st.text_input("Password", type="password", key="password_login")
    submit = st.button("Login")

    if submit:
        if verifica_usuario(email, password): 
            username = buscar_username(email)

            # Criar um log de autenticação
            conn = sqlite3.connect('dash/db/database.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO auth_logs (username, time, type)
            VALUES (?, datetime('now'), 'login')
            """, (username,))
            conn.commit()
            conn.close()


            st.session_state['user_name'] = username           
            st.success("Login realizado com sucesso!")
            return True
        else:
            st.error("Erro ao realizar login!")

            # Criar um log de autenticação
            conn = sqlite3.connect('dash/db/database.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO auth_logs (username, time, type)
            VALUES (?, datetime('now'), 'login')
            """, (email,))
            conn.commit()
            conn.close()

            
            return False